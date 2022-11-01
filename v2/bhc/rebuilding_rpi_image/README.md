# 노드 별 모델의 정상 작동을 위한 이미지 재구축
노드 별 동작 실험, 멀티 스테이지 빌드, 이미지 리빌드

## 같은 이미지를 타 노드에 배포하여 컨테이너 생성 및 동작 검증

### 1. NUC PC
>spec
>- name : w02
>- Intel AMD CPU
>- Ubuntu 20.04.5 LTS

#### Install docker
```bash
$ sudo apt update
$ sudo apt-get install -y ca-certificates \ 
    curl \
    software-properties-common \
    apt-transport-https \
    gnupg \
    lsb-release


$ sudo mkdir -p /etc/apt/keyrings
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

$ echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

#### env set, pull image, build container
```bash
## insecure-registry 설정 파일 생성 및 내용 추가
$ vi /etc/docker/daemon.json

>> {
			"insecure-registries" : ["192.168.0.208:5000"]
		}

## save file
:w !sudo tee % > /dev/null

## 파일 생성 후 docker 재실행
$ systemctl restart docker

## pull image
$ docker image pull 192.168.0.208:5000/edge_model:v1.0
# >> pulling from edge_model ...

## check images
$ docker images list

## build container
$ docker run -it %image_name
```
모델이 정상적으로 작동하는 것을 확인했습니다.

### 2. RPI
>spec
>- name : rpi6401
>- Debian GNU/Linux 11
>- ARM64/v8 CPU
>- ```$ ssh -p 39001 -l keti ketiabcs.iptime.org```

#### 이미지 재생성

##### install docker
```bash
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sh get-docker.sh
```

##### python base image
*docker hub에서 다운로드 받을 수 있는 official python image*<br>
<br>
multi-stage build를 지원하나 이미지를 통해 container를 build한 후에는 아키텍쳐 변경이 안되는 것으로 보입니다.<br>
rpi 내부에서 직접 python base-image를 pull한 후 모델 전달과 환경 구성을 세팅하고 커밋합니다.<br>
```bash
'''
RPI 환경 내부에서 작업
'''

## 전체 model 파일을 rpi 내부로 전송
scp -r final keti@192.168.0.241:/model

## base image download
$ docker pull python:3.8
>> Architecture : arm64로 자동 명시됨.

## build container
$ docker run -it python:3.8
$ docker cp ./model {container_id}:/home
$ docker rename {old_name} model
$ docker attach model

'''
지금부터 컨테이너 환경 내부
'''

$ pip install --upgrade pip

# pyotrch isntallation 참조 https://pytorch.org/get-started/locally/
$ pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

$ apt-get update
$ apt-get install vim

$ pip install -r requirements.txt

## 정상 작동 확인
$ python classifier.py
>> top5 출력
$ exit

## 지금부터는 라즈베리파이 커널입니다.
# push image into private registry
$ docker commit model 192.168.0.208:5000/rpi-model:1.0
$ docker push 192.168.0.208:5000/rpi-model:1.0

# repo list
$ curl -X GET http://192.168.0.208:5000/v2/_catalog
>> {"repositories":["edg_model","python","rpi-model"]}
```

## 차후 진행 방향성에 관하여

### multi-stage build image
컨테이너 빌드 시 연결된 노드의 CPU 아키텍쳐를 감지하여 자동으로 그에 맞게 명시하여 빌드되는 이미징 기술입니다.<br>
다양한 종류의 노드에 이미지를 배포하기 위해서는 멀티 스테이지 빌드를 지원하는 이미지를 사용하여 빌드한 뒤 환경을 구성하거나, 구성이 완료된 이미지를 커밋할 때 멀티 스테이지 빌드를 지원하도록 명시하거나 기술을 적용할 수 있는 방법론에 대한 조사가 필요합니다.

### Dockerfile
컨테이너 빌드 시 사용할 base-image, 구성 전 실행할 스크립트, 외부 시스템 마운트, 빌드가 완료된 컨테이너 안에서 실행할 내용 등을 명시할 수 있는 도커 스크립트 파일 포맷입니다.<br>
이미지 빌드나 배포를 위한 서버의 역할을 줄여줄 수 있으며 레지스트리 사용 또한 간소화할 수 있습니다.<br>
기본 이미지를 통해 빌드하면서 스토리지 마운트 및 다운로드를 통한 모델 서빙과 환경 구성을 스크립트로 자동화하여 노드 자체적으로 컨테이너를 구성하고 바로 모델을 작동시키는 것 까지 수행할 수 있을 것으로 생각됩니다.
