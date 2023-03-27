#!/bin/bash

## 이미지 이름과 태그
IMAGE_NAME="image_classification"
IMAGE_TAG="latest"

## Docker 이미지 빌드
docker build -t $IMAGE_NAME:$IMAGE_TAG .

## Docker registry 로그인
#echo "Enter your AAA Docker registry credentials:"
#docker login registry.aaa.com -u <USERNAME> -p <PASSWORD>

URL="ketiabcs.iptime.org:35050"

# Docker 이미지 푸시
docker tag $IMAGE_NAME:$IMAGE_TAG $URL/$IMAGE_NAME:$IMAGE_TAG
docker push $URL/$IMAGE_NAME:$IMAGE_TAG

docker tag image_classification:latest ketiabcs.iptime.org:35050:latest

# TODO
## Docker registry 로그아웃
#docker logout registry.aaa.com


curl -X GET $URL/v2/_catalog
# curl -X GET $URL/v2/hello-world/tags/list