import pika, sys, os
import time


def main():

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='binary_data')

    def callback(ch, method, properties, body):
        #print(" [x] Received %r" % body)
        print("[+] ok, received !")

        try:
            fname = time.strftime("%Y%m%d-%H%M%S.jpg")
            f=open(fname, "wb")
            f.write(body)
            f.close()
        
            print("[+] ok, saved !")
        except:
            print("[-] failed, file saving")

    channel.basic_consume(queue='binary_data', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)