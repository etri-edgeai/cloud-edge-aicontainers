import pika
from torch_model import Net

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue_torch')


def on_request(ch, method, props, body):
    n = int(body)
    print(f"[d, server] message from client = {n}")
    
    net = Net()
    response = net.state_dict()

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue_torch', on_message_callback=on_request)

print(" [+, server] Awaiting RPC requests, for torch model")
channel.start_consuming()