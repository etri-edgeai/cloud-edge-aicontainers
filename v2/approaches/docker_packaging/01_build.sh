#!/bin/bash

# 이미지 이름과 태그
IMAGE_NAME="image_classification"
IMAGE_TAG="latest"

# Docker 이미지 빌드
docker build -t $IMAGE_NAME:$IMAGE_TAG .


