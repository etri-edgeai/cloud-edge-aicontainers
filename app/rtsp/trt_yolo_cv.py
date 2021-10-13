"""trt_yolo_cv.py

This script could be used to make object detection video with
TensorRT optimized YOLO engine.

"cv" means "create video"
made by BigJoon (ref. jkjung-avt)
"""
# ffmpeg -i /dev/video1 -vcodec h264_nvmpi -f rtsp rtsp://localhost:8554/mystream


import os
import argparse
import time
import cv2
import pycuda.autoinit  # This is needed for initializing CUDA driver
import subprocess as sp
from utils.yolo_classes import get_cls_dict
from utils.visualization import BBoxVisualization
from utils.yolo_with_plugins import get_input_shape, TrtYOLO
from utils.display import open_window, set_display, show_fps

def parse_args():
    """Parse input arguments."""
    desc = ('Run the TensorRT optimized object detecion model on an input '
            'video and save BBoxed overlaid output as another video.')
    parser = argparse.ArgumentParser(description=desc)
    # parser.add_argument(
    #     '-v', '--video', type=str, required=True,
    #     help='input video file name')
    # parser.add_argument(
    #     '-o', '--output', type=str, required=True,
    #     help='output video file name')
    parser.add_argument(
        '-c', '--category_num', type=int, default=80,
        help='number of object categories [80]')
    parser.add_argument(
        '-m', '--model', type=str, required=True,
        help=('[yolov3|yolov3-tiny|yolov3-spp|yolov4|yolov4-tiny]-'
              '[{dimension}], where dimension could be a single '
              'number (e.g. 288, 416, 608) or WxH (e.g. 416x256)'))
    parser.add_argument(
        '-l', '--letter_box', action='store_true',
        help='inference with letterboxed image [False]')
    args = parser.parse_args()
    return args


def loop_and_detect(cap, trt_yolo, conf_th,vis,proc):#,writer):
    """Continuously capture images from camera and do object detection.

    # Arguments
      cap: the camera instance (video source).
      trt_yolo: the TRT YOLO object detector instance.
      conf_th: confidence/score threshold for object detection.
      vis: for visualization.
      writer: the VideoWriter object for the output video.
    """
    fps = 0.0
    tic = time.time()
    while True:
        ret, frame = cap.read()
        if frame is None:  break
        boxes, confs, clss = trt_yolo.detect(frame, conf_th)
        frame = vis.draw_bboxes(frame, boxes, confs, clss)
        frame = show_fps(frame, fps)

        # cv2.imshow("image",frame)

        toc = time.time()
        curr_fps = 1.0 / (toc - tic)
        # calculate an exponentially decaying average of fps number
        fps = curr_fps if fps == 0.0 else (fps*0.95 + curr_fps*0.05)
        tic = toc
        proc.stdin.write(frame.tobytes())
        # writer.write(frame)
        # print('.', end='', flush=True)
        key = cv2.waitKey(1) #wait 1ms the loop will start again and we will process the next frame
    
        if key == 27: #esc key stops the process
            break
    print('\nDone.')


def main():
    args = parse_args()
    if args.category_num <= 0:
        raise SystemExit('ERROR: bad category_num (%d)!' % args.category_num)
    if not os.path.isfile('yolo/%s.trt' % args.model):
        raise SystemExit('ERROR: file (yolo/%s.trt) not found!' % args.model)
    rtsp_url = "rtsp://localhost:8554/cam"
    cap = cv2.VideoCapture(0)
    cap.set(3,1280) 
    cap.set(4,720)
    if not cap.isOpened():
        raise SystemExit('ERROR: failed to open the input video file!')
    frame_width, frame_height = int(cap.get(3)), int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
 
    command = ['ffmpeg',
           '-y',
           '-f', 'rawvideo',
           #'-vcodec', 'rawvideo',
           '-pix_fmt', 'bgr24',
           '-s', "{}x{}".format(frame_width, frame_height),
           '-r', str(fps),
           '-i', '-',
           '-c:v', 'h264_nvmpi',
           #'-pix_fmt', 'yuv420p',
           '-preset', 'ultrafast',
           '-f', 'rtsp',
           rtsp_url]

    proc = sp.Popen(command, stdin=sp.PIPE)
    cls_dict = get_cls_dict(args.category_num)
    vis = BBoxVisualization(cls_dict)
    # h, w = get_input_shape(args.model)
    trt_yolo = TrtYOLO(args.model, args.category_num, args.letter_box)

    loop_and_detect(cap, trt_yolo, conf_th=0.3, vis=vis,proc = proc) #, writer=writer)

    # writer.release()
    cap.release()
    proc.stdin.close()
    proc.stderr.close()
    proc.wait()


if __name__ == '__main__':
    main()
