# AI 모델 도커 가상환경 구축
**모델이 동작할 컨테이너 가상 환경 구축**

### Build Docker Container
```bash
## Base-image from Docker hub
$ docker pull python:3.8

$ docker images
$ docker run -it python:3.8 bash

## send model from host to container
$ docker cp {model_dir} {container_id}:{dir}
```

### Packages
```bash
pip install -r requirements.txt
```
Pytorch의 경우 해당 환경에 맞는 명령을 통해 별도 설치합니다.
```bash
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
```
>Pytorch Installation 참조 : https://pytorch.org/get-started/locally/

### 기타 조작
```bash
## 이미 빌드된 컨테이너 시작
$ docker start {container_name}
## 실행 중인 컨테이너에 쉘 연결
$ docker attach {container_name}
## 재실행
$ docker restart {container_name}
## 이름 변경
docker rename {old_name} {new_name}
```
