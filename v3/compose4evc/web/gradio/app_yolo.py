import gradio as gr
import time
from PIL import Image
import torch
from ultralytics import YOLO
import yaml
from yaml import load, dump
from yaml.loader import SafeLoader, BaseLoader, FullLoader, UnsafeLoader
import numpy as np
import cv2 
import onnxruntime as ort
import requests
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

########################################################################################################## COCO Class List #####
coco_128_class_list = ['aeroplane', 'backpack', 'banana', 'baseball bat', 'baseball glove', #5
'bear', 'bed', 'bench', 'bicycle', 'bird', 
'boat', 'book', 'bottle', 'bowl', 'broccoli', 
'bus', 'cake', 'car', 'carrot', 'cat', 
'cell phone', 'chair', 'clock', 'cup', 
'diningtable','dog', 'donut', 'elephant', 'fork',
'frisbee', 'giraffe', 'handbag', 'horse', 'hot dog',
 'kite', 'knife', 'laptop', 'microwave', 'motorbike', 
 'mouse', 'orange', 'oven', 'person', 'pizza', 
 'pottedplant', 'refrigerator', 'remote', 'sandwich', 'scissors', 
 'sink', 'skateboard', 'skis', 'snowboard', 'sofa', 
 'spoon', 'sports ball', 'stop sign', 'suitcase', 'teddy bear', 
 'tennis racket', 'tie', 'toilet', 'toothbrush', 'traffic light', 
 'train', 'truck', 'tvmonitor', 'umbrella', 'vase',
 'wine glass', 'zebra']   # 71개 

########################################################################################################## Model 정의 #####
# 기본 모델 사용해서 테스트를 진행했습니다. 
#GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# YOLO
model_yolo = YOLO("yolov8n.yaml")  # build a new model from scratch
model_yolo = YOLO('yolov8s.pt')
model_yolo.to(device)
# Image Captioning
model_vit = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
model_vit.to(device)

########################################################################################################## 파라미터 정의 #####
max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

model_path = 'yolov8s.pt' # yolo 훈련시키기 전에 사진 넣었을 경우를 대비하여 기본값 설정 
########################################################################################################## Function 정의 #####
# Function 1 : Image Caption
def predict_step(img_path):
    images = Image.open(img_path)
    
    pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)
    
    output_ids = model_vit.generate(pixel_values, **gen_kwargs)
    
    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    global sentence
    sentence = preds[0]
    return sentence

# Function 2 : 사용자가 Text입력했을 때 History에 저장하는 과정 
def add_text(history, text):
    history = history + [(text, None)] # 여기서 text는 user 질문
    print("addtext", history)
    return history, gr.update(value="", interactive=False) # 어떤 행동을 했을 때 value=""로 바꿔라. # interactive?

# Function 3 : 사용자가 file upload했을 때 History에 저장하는 과정 
def add_file(history, file):
    history = history + [((file.name,),None)]
    print("addfile", history)
    return history

# Function 4 : 사용자의 입력에 따라 YOLO train을 진행하거나 오류 메세지를 내보내는 과정 
def bot(history):
    ### 사용자가 Text를 입력했을 때 (=입력이 사진이 아닐 때) 
    if history[-1][0][0].lower().endswith(('.jpg', '.png', 'jpeg')) == False : # 입력이 사진이 아닐 때 
        ### 입력으로 들어온 단어가 COCO Class 리스트에 있다면,
        if history[-1][0].lower() in coco_128_class_list:  
            input_class = history[-1][0]
            ### 1. yaml파일 수정 
            ### 미리 만들어둔 빈 yaml파일 활용 
            with open('./empty.yaml', 'r') as f:
                data = yaml.load(f, Loader = SafeLoader)
                data['names'].append(input_class) 
                data['nc'] = len(data['names'])
    
            ### 새로운 yaml파일 생성
            with open(f'{input_class}.yaml', 'w') as g:
                print("yaml파일 data", data)
                yaml.dump(data, g, sort_keys=False, default_flow_style=False)
    
            ### YOLO 훈련
            yaml_path = f'./{input_class}.yaml'
            model_yolo.train(data=yaml_path, epochs=3)
            
            global model_path
            model_path = model_yolo.export()  #모델을 저장하자 
            model_path = model_path.split('.')[0]+'.pt'
            print('모델경로', model_path)
            
            response = "***Finished Training***"
            print('response한 후',history)
            history[-1][1] = ""
            print('history[-1][1] = ""', history)
            for character in response:
                history[-1][1] += character
                time.sleep(0.05)
                yield history

        ### COCO list에 없는 문자를 입력 받았을 때 
        else:
            response = "***sorry we can't train that object class***"
            print('response한 후',history)
            history[-1][1] = ""
            print('history[-1][1] = ""', history)
            for character in response:
                history[-1][1] += character
                time.sleep(0.05)
                yield history 

    ### 사용자가 사진을 upload했을 경우 
    elif history[-1][0][0].lower().endswith(('.jpg', '.png', 'jpeg')) == True : # 사진일 때 
        ### 1. YOLO
        global img_path
        img_path = history[-1][0][0]
        model_detect = YOLO(model_path)
        model_detect.to(device)
        results = model_detect(img_path)
        img = results[0].plot()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Image.fromarray를 쓸 때 output 이미지의 색이 바뀌는 것을 방지 
        img = Image.fromarray(img)
        img.save('yoloresult.jpg')
        response = ["yoloresult.jpg"]  # list 안에 담아줘야함 
        history[-1][1] = response # history[-1][1] = bot 응답 넣는 칸 
        print(history)
        yield history

### YOLO 결과를 응답으로 내보낸 후, 바로 Image Caption의 결과를 응답으로 내보냄 
def botbot(history):
    ### 2. Img Caption 
    predict_step(img_path)
    response2 = sentence 
    history = history + [[None, 'text']] 
    history[-1][1] = response2
    yield history
            
########################################################################################################## Chatbot 화면 구성 #####
with gr.Blocks() as demo:
    chatbot = gr.Chatbot( elem_id="chatbot").style(height=900) # 채팅방 높이 

    with gr.Row():
        with gr.Column(scale=0.85):
            txt = gr.Textbox(
                show_label=False,
                placeholder="Enter text and press enter, or upload an image",scale=2).style(container=False)
        with gr.Column(scale=0.15, min_width=0):
            btn = gr.UploadButton("📁", file_types=["image", "video", "audio"])

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=True).then(
        bot, chatbot, chatbot
    )
    txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=True)
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=True).then(
        bot,chatbot, chatbot
    )
    file_msg.then(botbot, chatbot, chatbot)


#demo.queue().launch(share=True, debug=True, inline=False)
demo.queue().launch(debug=True, 
            root_path="/chatbot",
            server_name="0.0.0.0")