# AI Repository


## AI Repository를 생성하기

- Docker hub 에서 registry 이미지를 찾습니다.
```bash
 $ docker search registry
```

- Registry 이미지를 다운로드 받습니다.

```bash
$ docker pull registry:latest
```

- Registry 이미지를 잘 다운로드 받았는지 확인합니다.

```bash
$ docker images registry
```

- Registry Docker 이미지를 실행합니다. 이때 포트번호는 서비스 설정 파일에 의해 변경될 수 있습니다.

```bash
$ docker run --name airegistry -d -p 3001:5000 registry
```

- 컨테이너가 잘 실행되는지 확인해 봅니다.

```bash
 $ docker ps | grep registry
```

- 서비스에 직접 접근하여 기능 동작이 되는지를 터미널에서 확인해 봅니다. 여기서는 cURL을 사용합니다. 터미널에 응답이 온다면 서비스가 동작하고 있다는 의미입니다.

 . 참고로 curl -v 의 경우 "디버깅을 위해 요청과 응답 헤더까지 모두 표시"하라는 의미입니다.

```bash
$ curl -v localhost:3001
```

- (옵션) 종료 및 삭제는 다음과 같이 합니다.
```bash
$ docker container stop airegistry 
$ docker container rm -v airegistry
```

## AI Repository에 업로드할 이미지를 빌드하고 동작을 시험하기

- airepository에 업로드할 샘플 docker image를 만들어 봅니다.

```bash
$ vi Dockerfile
```

```bash
FROM ubuntu:latest
CMD echo 'Hello, new world!'
```

```bash
$ docker build --tag myhello/myhello-tag .
```

- airepository에 업로드할 샘플 docker image를 확인합니다.

```bash
$ docker images | grep myhello
```

- airepository에 업로드할 샘플 docker image의 동작을 확인합니다.

```bash
$ docker run myhello/myhello-tag
```

- 실제로는 상기의 빌드과정과 시험과정은 원하는 결과를 얻을 수 있도록 반복적으로 실행될 것입니다.


## AI Repository에 이미지를 업로드(push)하기

- 업로드할 샘플 docker image를 "airegistry"라는 이름으로 만든 private docker registry에 등록하겠습니다.

- 먼저 tag를 추가하기 위한 명령어는 아래와 같은 형식을 갖습니다.

```bash
docker tag 원본이미지(:tag) {원격주소:포트/}{프로젝트)/이미지(:tag)
```

- tag를 추가하는 명령어는 다음과 같습니다.

```bash
$ docker tag myhello/myhello-tag localhost:3001/myhello-tag
```

- "airegistry"라는 이름으로 만든 private docker registry에 push를 통해 등록합니다.

```bash
$ docker push localhost:3001/myhello-tag
```

- 아래와 같은 명령어를 수행하여 "airegistry"라는 이름으로 만든 private docker registry에 등록된 모델을 RESTAPI를 통해 확인합니다.

```bash
$ curl -X GET http://localhost:3001/v2/_catalog
```

- 아마도 아래와 같은 목록이 확인될 것입니다.

```bash
{"repositories":["myhello-tag"]}
```

- 다음과 같은 명령어를 통해서도 확인이 가능합니다.

```bash
$ curl -X GET http://localhost:3001/v2/myhello-tag/tags/list
```



## AI Repository에 업로드(push)한 이미지를 당겨오기(pull) 합니다.

- "airepository"에 업로드한 "myhello" 이미지를 다운로드 받겠습니다.

- 이를 위해 이미 local에 존재하는 "myhello" 이미지는 삭제합니다.

```bash
$ docker rmi myhello/myhello-tag localhost:3001/myhello-tag
```

- "myhello" 이미지가 잘 삭제되었는지 확인합니다.

```bash
$ docker images | grep myhello
```

- local 에 설치한 "airepository"에 등록된 "myhello" 를 다운로드 및 실행합니다. "docker run"을 하면 해당 이미지가 없다면 다운로드후에 실행합니다.

```bash
docker run localhost:3001/myhello-tag
```

- "myhello" 이미지를 다시 확인합니다.

```bash
$ docker images | grep myhello
```

## AI Repository 를 UI에서 확인하기

- 아래 주소를 참고하여 진행합니다.

```bash

https://hub.docker.com/r/joxit/docker-registry-ui

https://engineering.linecorp.com/ko/blog/harbor-for-private-docker-registry/

```





