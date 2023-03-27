import torch
import requests
from io import BytesIO
from PIL import Image
from torchvision import transforms
from flask import Flask, jsonify, request

# 모델 다운로드 및 로드
model_url = 'http://example.com/model.pth'
model = torch.hub.load_state_dict_from_url(model_url, map_location=torch.device('cpu'))

# 이미지 전처리
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# 이미지 분류 함수
def predict_image(image_bytes, model):
    # 이미지 로드 및 전처리
    image = Image.open(BytesIO(image_bytes))
    image_tensor = preprocess(image).unsqueeze(0)
    
    # 분류 예측
    with torch.no_grad():
        output = model(image_tensor)
        output = torch.softmax(output, dim=1)
    
    # 결과 반환
    class_idx = torch.argmax(output).item()
    score = output[0][class_idx].item()
    return class_idx, score

# Flask 웹 애플리케이션
app = Flask(__name__)

@app.route('/classify', methods=['POST'])
def classify_image():
    # 이미지 파일 읽기
    file = request.files['image']
    image_bytes = file.read()
    
    # 이미지 분류 예측
    class_idx, score = predict_image(image_bytes, model)
    
    # 결과 반환
    class_name = 'apple' if class_idx == 0 else 'strawberry'
    return jsonify({'class_name': class_name, 'score': score})


