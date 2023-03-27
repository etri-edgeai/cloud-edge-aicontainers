# Docker 이미지 생성
FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY app.py .

CMD ["python3", "app.py"]