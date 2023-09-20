# syntax=docker/dockerfile:1

# reference : https://docs.docker.com/compose/gettingstarted/

FROM python:3.8.10
WORKDIR /code

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN apt-get update && apt-get -y install libgl1-mesa-glx
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8010
COPY . .
CMD ["flask", "run", "--host=0.0.0.0", "--port=8010", "--debug"]