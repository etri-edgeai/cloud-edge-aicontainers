from celery import Celery
import time

app = Celery('tasks', broker='amqp://')


@app.task()
def add(x, y):
    print("<start>")
    time.sleep(5)
    r = x + y
    print("<end>")
    return r


if __name__ == '__main__':
    app.start()