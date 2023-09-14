# syntax=docker/dockerfile:1
# reference : https://docs.docker.com/compose/gettingstarted/
From python:3.9

RUN mkdir _output
COPY ./_output/iris.onnx ./_output/iris.onnx
COPY app.py app.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8011
CMD ["uvicorn", "app:app", "--reload", "--host=0.0.0.0", "--port=8011"]