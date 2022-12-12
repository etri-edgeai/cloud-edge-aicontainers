## Dockerfile
**Dockerfile?? : ```docker build``` 커맨드 수행 시 이미지 생성 절차에 대한 명시**<br>
<br>
새로운 노드와 호환, 다른 종류의 모델이 요구될 때 자동으로 이미지를 구축하기 위한 image build 용 스크립트입니다.<br>

### 스크립트 구성
- base image 호출
  - CPU architecture 간 호환을 위한 multi-architecture build를 지원하는 이미지를 base-image로 설정해야 합니다.
- model download
  - model.tar.gz 파일을 가상 환경 내부로 복사합니다. 반드시 tar 포맷이어야 합니다.
- packages installation
  - 가상 컨테이너에 환경을 구성합니다. model.tar.gz에 requirments.txt가 포함되어 있어야 합니다.


### 스크립트 실행
Dockerfile과 model.tar.gz가 위치한 경로에서 수행합니다.<br>
```bash
$ docker build --tag dockerfile-test:1.0 .
$ docker run -d --name dockerfile-test -it dockerfile-test:1.0
$ docker exec dockerfile-test python home/classifier.py
```
### 실행 결과
![](../img4doc/dockerfile1.png)
![](../img4doc/dockerfile2.png)
