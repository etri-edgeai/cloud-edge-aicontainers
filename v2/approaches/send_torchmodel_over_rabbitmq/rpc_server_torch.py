import pika
from torch_model import Net

import torch
import torchvision # model을 불러오기 위해 import 하였습니다.


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue_torch')


def on_request(ch, method, props, body):
    n = int(body)
    print(f"[d, server] message from client = {n}")
    
    if n == 0:
        model = Net()
        params = model.state_dict()
    else:
        # 1. 임의의 model을 사용해도 되며, 실제 사용하는 custom model을 불러와서 저장해 보시기 바랍니다.
        model = torchvision.models.vgg16(pretrained=False)

        # 2. model의 파라미터를 OrderedDict 형태로 저장합니다.
        params = model.state_dict()

    response = {'model':model, 'params':params}

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response) )
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue_torch', on_message_callback=on_request)

print(" [+, server] Awaiting RPC requests, for torch model")
channel.start_consuming()