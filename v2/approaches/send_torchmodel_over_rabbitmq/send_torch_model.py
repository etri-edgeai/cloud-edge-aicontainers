import torch
import torchvision # model을 불러오기 위해 import
import torch.onnx

def make_vgg16_model(fname):
    # 1. 실제 사용하는 custom model을 불러와서 저장 가능
    model = torchvision.models.vgg16(pretrained=False)

    # 2. model의 파라미터를 OrderedDict 형태로 저장
    params = model.state_dict()

    # 3. 동적 그래프 형태의 pytorch model을 위하여 data를 model로 흘려주기 위한 더미 데이터 주입
    dummy_data = torch.empty(1, 3, 224, 224, dtype = torch.float32)

    # 4. onnx 파일을 export 함. 함수에는 차례대로 model, data, 저장할 파일명 순서대로 입력
    torch.onnx.export(model, dummy_data, fname)


import pika

fname = "send.onnx"
#make_vgg16_model(fname)
#fname = "apple.png"

with open(fname, "rb") as f:
    data = f.read()
    
TODO : 대용량 파일 전송은 안되고 있음. JPark


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='torch_model')

channel.basic_publish(exchange='',routing_key='torch_model',body=data)
print("[+] Sent image")
connection.close()



