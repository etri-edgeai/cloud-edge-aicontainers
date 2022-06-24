from ctypes import *
import random
import os
import cv2
import time
import darknet
import argparse
from threading import Thread, enumerate
from queue import Queue

import logging

## Suppress Deprecated Warnings
import sys
if not sys.warnoptions:
	import warnings
	warnings.simplefilter("ignore")

mask_map = {
    "Ceiling_Cam"   : "ceiling",
    "Pen_B"         : "penb",
    "Pen_C"         : "penc"    
}

class MyModel:
    def __init__(self):
        """
        """
        self.interval = 30.0 
        self.image_queue = Queue() 
        self.result_queue = Queue()

    def load_ai_model(self, filename):

        return 0

    def convert2original(self, image, bbox): 
        x, y, w, h = self.convert2relative(bbox) 
        image_h, image_w, __ = image.shape

        orig_x       = int(x * image_w)
        orig_y       = int(y * image_h)
        orig_width   = int(w * image_w)
        orig_height  = int(h * image_h)

        bbox_converted = (orig_x, orig_y, orig_width, orig_height)

        return bbox_converted


    def convert2relative(self,bbox):
        """
        YOLO format use relative coordinates for annotation
        """
        x, y, w, h  = bbox
        _height     = self.darknet_height
        _width      = self.darknet_width
        return x/_width, y/_height, w/_width, h/_height

    """ image processing thred """
    def process_frame(self):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        print (self.video_fps, " + ", self.w, "+", self.h)
        out = cv2.VideoWriter(f"annotatedvideo.mp4", fourcc, self.video_fps, (self.w, self.h))
        count = 0

        random.seed(3)  # deterministic bbox colors

        while True:
            print( "reading input queue: " + str(self.image_queue.qsize()))
            if (self.image_queue.qsize() == 0 and count != 0):
                print( "input q emty!")
                out.release()
                return 1
            else:
                frame = self.image_queue.get()
                print( "processing a frame in a thread")
                print( "***remaining input queue size: " + str(self.image_queue.qsize()))
            
            """
            while not self.image_queue.empty():
                self.image_queue.get()
            """
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (self.darknet_width, self.darknet_height),
                                   interpolation=cv2.INTER_LINEAR)
                    
            img_for_detect = darknet.make_image(self.darknet_width, self.darknet_height, 3)
            prev_time = time.time()
            darknet.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())
            detections = darknet.detect_image(self.network, self.class_names, img_for_detect, thresh=0.25)

            darknet.free_image(img_for_detect)

            detections_adjusted = []

            for label, confidence, bbox in detections:
                bbox_adjusted = self.convert2original(frame, bbox) 
                detections_adjusted.append((str(label), confidence, bbox_adjusted))
            image = darknet.draw_boxes(detections_adjusted, frame, self.class_colors)
            count+=1
            print('now saving to a file')
            out.write(image)


    def read_frame(self):
        print("reading video file...")
        while True:
            ret, frame= self.cap.read()

            if ret:
                if (self.image_queue.qsize() > 200):
                    while True:
                        logging.info('input queue too big. wait for queue clear')
                        time.sleep (0.1)
                        if (self.image_queue.qsize() < 200):
                            break
                self.output_index = self.output_index + 1
                #logging.debug("video frame acquired...")
                """
                if ( self.output_index % self.interval ) != 0:
                    #logging.info("ignoring this frame")
                    continue
                """

                # put into input queue
                self.image_queue.put( frame )
                logging.info("put the frame into input queue...")
            else:
                logging.info ("no video")
                self.cap.release()
                return 0

  
    def write_frame(self):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        print (self.video_fps, " + ", self.w, "+", self.h)
        out = cv2.VideoWriter("annotatedvideo.mp4", fourcc, self.video_fps, (self.w, self.h))
    
        while True:
            try:
                #logging.info( "waiting for result queue")
                results = self.result_queue.get_nowait()
                out.write(results)
            except queue.Empty:
                #logging.warning( "out q empty. continue")
                continue            

    def compute_ai(self, *args):
        if ( args[0].startswith ('file')): # for test purpose only
            filename = args[0].split('/')[-1]
        else:
            filename = args[0]


        self.network, self.class_names, self.class_colors = darknet.load_network( './cfg/yolov4.cfg', './cfg/coco.data', './networks/yolov4.weights', batch_size = 1)

        self.darknet_width = darknet.network_width(self.network)
        self.darknet_height = darknet.network_height(self.network)

        self.cap = cv2.VideoCapture(filename)

        video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.w, self.h, self.video_fps = int(self.cap.get(3)), int(self.cap.get(4)), self.cap.get(5)
       
        total_frames = 0
       
        self.output_index = 1
        
        if ('processing_thread' in locals() ):
            logging.debug("thread already running")
            return "NOT SUPPORTED"
        else:
            logging.info("------------starting image thread-------------")
            self.processing_thread = Thread(target = self.process_frame)
            self.processing_thread.start()
                
        if ('reader_thread' in locals() ):
            logging.debug("reader thread already running")
            return "NOT SUPPORTED"
        else:
            logging.info("------------starting reader thread-------------")
            self.reader_thread = Thread(target = self.read_frame)
            self.reader_thread.start()

        """ 
        if ('writer_thread' in locals() ):
            logging.debug("writer thread already running")
            return "NOT SUPPORTED"
        else:
            logging.info("------------starting writer thread-------------")
            self.writer_thread = Thread(target = self.write_frame)
            self.writer_thread.start()
        """

        print("video device open...")
        return 0

    def compute_ai_stream(self, *args):
        if ( args[0].startswith ('file')): # for test purpose only
            filename = args[0].split('/')[-1]
        else:
            filename = args[0]

        count = 0

        self.network, self.class_names, self.class_colors = darknet.load_network( './cfg/yolov4.cfg', './cfg/coco.data', './networks/yolov4.weights', batch_size = 1)

        self.darknet_width = darknet.network_width(self.network)
        self.darknet_height = darknet.network_height(self.network)

        self.cap = cv2.VideoCapture(filename)

        video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.w, self.h, self.video_fps = int(self.cap.get(3)), int(self.cap.get(4)), self.cap.get(5)
       
        total_frames = 0
       
        self.output_index = 1

        print("reading video file...")
        while True:
            ret, frame= self.cap.read()

            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_resized = cv2.resize(frame_rgb, (self.darknet_width, self.darknet_height),
                                       interpolation=cv2.INTER_LINEAR)
                        
                img_for_detect = darknet.make_image(self.darknet_width, self.darknet_height, 3)
                prev_time = time.time()
                darknet.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())
                detections = darknet.detect_image(self.network, self.class_names, img_for_detect, thresh=0.25)

                darknet.free_image(img_for_detect)

                detections_adjusted = []

                for label, confidence, bbox in detections:
                    bbox_adjusted = self.convert2original(frame, bbox) 
                    detections_adjusted.append((str(label), confidence, bbox_adjusted))
                image = darknet.draw_boxes(detections_adjusted, frame, self.class_colors)
                count+=1
                print('now saving to a file')

                frame_out = cv2.imencode('.jpg', image)[1].tostring()

                yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_out + b'\r\n')

            else:
                logging.info ("no video")
                self.cap.release()
                return 0

    def stop_ai(self, *args):

        self.reader_thread.join()
        self.processing_thread.join()
        #self.writer_thread.join()
