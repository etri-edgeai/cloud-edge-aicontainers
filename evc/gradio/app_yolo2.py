import gradio as gr
import torch 
from PIL import Image
from ultralytics import YOLO
import numpy as np
import cv2 
import requests
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

# Images
torch.hub.download_url_to_file('https://github.com/ultralytics/yolov5/raw/master/data/images/zidane.jpg', 'zidane.jpg')
torch.hub.download_url_to_file('https://github.com/ultralytics/yolov5/raw/master/data/images/bus.jpg', 'bus.jpg')

#Model define ############## 기본 모델을 사용하였음 -> 모델 변경해야함.
model_yolo = YOLO('yolov8s') 
model_vit = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
model = model_yolo

#GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# gradio.Interface에 쓰일 function이 필요함
# fuction 1 : Image Caption 모델 
max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

def predict_step(images):

    pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)
    
    output_ids = model.generate(pixel_values, **gen_kwargs)
    
    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    return preds[0]

#function 2 : YOLO 모델 
def yolo(im, size=640):
    results = model_yolo(im)
    img = results[0].plot()
    original_shape = results[0].orig_shape
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Image.fromarray를 쓸 때 output 이미지의 색이 바뀌는 것을 방지 
    img = Image.fromarray(img)
    # m = size / max(img.size)
    # img = img.resize((int(x * g) for x in img.size) # resize
    return img


# gr.Interface에 쓰일 input, output 정의 
input = gr.inputs.Image(type="pil",label="Original Image") 
output = gr.outputs.Image( type="pil",label="Output Image")

# 2개의 Interface 정의
# input은 2개의 모델에 동일한 input을 쓴다. (하나의 사진을 받아서 2개의 모델로 결과를 냄) 
yolo_interface = gr.Interface(yolo, inputs= input, outputs =output, analytics_enabled=False)
img_caption_interface = gr.Interface(predict_step, inputs = input, outputs="text")

# 두 모델의 interface를 하나로 합쳐서 웹으로 launch한다. 
demo = gr.Parallel(yolo_interface, img_caption_interface)

if __name__ == "__main__":
    #demo.launch(share=True)
    
    demo.queue().launch(debug=True, 
            root_path="/infer02",
            server_name="0.0.0.0")