# Make NN model

# by JPark @ 2022
# - gRPC로 신경망 모델을 전달하는 실험을 위해 기 학습된 모델을 저장합니다.
# - 서버와 클라이언트 상호간에 전달을 수행하며, "Netron" 유틸리티로 확인합니다.

import os

def makedir(path): 
    try: 
        os.makedirs(path)
        
    except OSError: 
        if not os.path.isdir(path): 
            raise
    
    return os.path.abspath(path)


makedir('server/dataset/0/') # 저장할 공간


#----------------------------------------------------------------------
## vgg16
#----------------------------------------------------------------------
import torch
import torchvision
import torch.onnx

# 1. 실제 사용하는 custom model을 불러와서 저장 가능
model = torchvision.models.vgg16(pretrained=False)

# 2. model의 파라미터를 OrderedDict 형태로 저장
params = model.state_dict()

# 3. 동적 그래프 형태의 pytorch model을 위하여 data를 model로 흘려주기 위한 더미 데이터 주입
dummy_data = torch.empty(1, 3, 224, 224, dtype = torch.float32)

# 4. onnx 파일을 export 함. 함수에는 차례대로 model, data, 저장할 파일명 순서대로 입력
torch.onnx.export(model, dummy_data, "server/dataset/0/vgg16.onnx")


#----------------------------------------------------------------------
## Resnet, pth file
#----------------------------------------------------------------------


# Save pth file
import torch

# model_names = ['resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152']
model_names = ['resnet18', 'resnet34', 'resnet50']

for name in model_names:
    model = torch.hub.load('pytorch/vision:v0.10.0', name, pretrained=True)

    PATH = "server/dataset/0/" + name + '.pth'
    torch.save(model.state_dict(), PATH)


#----------------------------------------------------------------------
## Resnet, onnx file
#----------------------------------------------------------------------

import torch
import torch.onnx 

# model_names = ['resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152']
model_names = ['resnet18', 'resnet34', 'resnet50']

for name in model_names:
    PATH = "server/dataset/0/" + name + '.onnx'
    
    model = torch.hub.load('pytorch/vision:v0.10.0', name, pretrained=True)
    #model.eval()

    # 동적 그래프 형태의 pytorch model을 위하여 data를 model로 흘려주기 위한 더미 데이터 주입
    dummy_data = torch.empty(1, 3, 224, 224, dtype = torch.float32)

    # onnx 파일을 export 함. 함수에는 차례대로 model, data, 저장할 파일명 순서대로 입력
    torch.onnx.export(model, dummy_data, PATH)



