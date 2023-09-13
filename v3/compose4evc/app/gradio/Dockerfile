From python:3.8.10

COPY requirements.txt requirements.txt
COPY app_yolo1.py app.py
#COPY app.py app.py

RUN apt-get update && apt-get -y install libgl1-mesa-glx
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["gradio", "app.py"]