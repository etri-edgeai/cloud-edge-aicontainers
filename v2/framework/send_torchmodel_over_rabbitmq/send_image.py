import pika

f=open("apple.png", "rb")
img=f.read()

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='binary_data')

channel.basic_publish(exchange='',routing_key='binary_data',body=img)
print("[+] Sent image")
connection.close()


