import torch
import torchvision.transforms as transforms
import urllib
from PIL import Image

# 모델 다운로드
model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
model.eval()

# 이미지 전처리
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# 이미지 다운로드 및 전처리
url, filename = ("https://github.com/pytorch/hub/raw/master/images/dog.jpg", "dog.jpg")
try: urllib.URLopener().retrieve(url, filename)
except: urllib.request.urlretrieve(url, filename)
input_image = Image.open(filename)
input_tensor = transform(input_image)
input_batch = input_tensor.unsqueeze(0)  # 배치 차원 추가

# 모델 추론
with torch.no_grad():
    output = model(input_batch)
    prediction = torch.nn.functional.softmax(output[0], dim=0)
    _, predicted_class = torch.max(output.data, 1)

# 결과 출력
print(f"Predicted class: {predicted_class.item()}")
print(f"Probability: {prediction[predicted_class].item() * 100:.2f}%")
