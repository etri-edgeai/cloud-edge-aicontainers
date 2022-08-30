import pika
import uuid

import argparse

class TorchModelRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue_torch',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        self.connection.process_data_events(time_limit=None)
        return self.response
        

def main() -> None:
    parser = argparse.ArgumentParser(description="rpc")
    parser.add_argument(
        "--num",
        type=int,
        default=30,
        required=False,
        help="tba",
    )
    args = parser.parse_args()
    
    
    torch_model_rpc = TorchModelRpcClient()

    print(f" [d, client] Requesting send torch model ({args.num})")
    response = torch_model_rpc.call(args.num)
    print(response)


if __name__ == "__main__":
    main()
