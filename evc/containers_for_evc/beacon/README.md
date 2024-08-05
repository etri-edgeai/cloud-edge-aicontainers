# beacon 스크립트

- 여러 아키텍처의 에지 기기에서 모니터링 정보를 evc서버로 전달하는 기능을 수행함



## 코드 설명

- 여러 에지 아키텍처를 지원하는 Docker 이미지를 만들고, 특정 아키텍처에서 특정 스크립트가 실행되게 함
- docker의 buildx를 사용하여 멀티 아키텍처 이미지를 빌드하고, 각 아키텍처에서 적절한 스크립트를 실행함

### 디렉토리 구조
```bash
.
├── beacon_arm.sh
├── beacon_x86.sh
├── Dockerfile
└── docker-compose.yml
```

### 스크립트 파일

- `beacon_arm.sh`와 `beacon_x86.sh` 파일로 구성됨
- 실제 내부 코드는 다름

1. `beacon_arm.sh`

```sh
#!/bin/sh
echo "Running on ARM architecture"
# ARM-specific commands here
```

2. `beacon_x86.sh`

```sh
#!/bin/sh
echo "Running on x86 architecture"
# x86-specific commands here
```

### Dockerfile

- 다음 `Dockerfile`은 두 아키텍처를 지원하는 이미지를 생성합니다.

```dockerfile
# Dockerfile
FROM alpine:latest

# Copy scripts into the image
COPY beacon_arm.sh /usr/local/bin/beacon_arm.sh
COPY beacon_x86.sh /usr/local/bin/beacon_x86.sh

# Make scripts executable
RUN chmod +x /usr/local/bin/beacon_arm.sh /usr/local/bin/beacon_x86.sh

# Set entrypoint based on the architecture
CMD ["/bin/sh", "-c", "if [ $(uname -m) = 'x86_64' ]; then /usr/local/bin/beacon_x86.sh; else /usr/local/bin/beacon_arm.sh; fi"]
```

### Docker Buildx 설치 및 설정

1. Docker Buildx 플러그인을 활성화합니다.

```sh
docker buildx create --use
```

2. 사용할 수 있는 빌더 목록을 확인합니다.

```sh
docker buildx ls
```

### 멀티 아키텍처 이미지 빌드 및 푸시

Docker Hub에 이미지를 푸시할 수 있도록 로그인한 상태여야 합니다.

```sh
docker buildx build --platform linux/amd64,linux/arm64 -t myusername/beacon:latest --push .
```

### Step 6: Docker Compose 파일 작성

`docker-compose.yml` 파일을 작성하여 멀티 아키텍처 이미지를 실행합니다.

```yaml
version: '3'
services:
  beacon_service:
    image: myusername/beacon:latest
    deploy:
      replicas: 1
    networks:
      - beacon_net

networks:
  beacon_net:
```

### Docker Compose로 실행

Docker Compose를 사용하여 서비스를 실행합니다.

```sh
docker-compose up -d
```

이 예제는 다음과 같은 동작을 합니다:
- Dockerfile은 두 스크립트를 이미지에 포함하고, 실행 시 시스템의 아키텍처를 확인하여 적절한 스크립트를 실행합니다.
- `docker buildx`를 사용하여 멀티 아키텍처 이미지를 빌드하고 Docker Hub에 푸시합니다.
- `docker-compose`를 사용하여 이미지를 실행하고, 적절한 스크립트를 실행합니다.

이제 Raspberry Pi와 x86 기반 컴퓨터에서 각각 적절한 스크립트가 실행되는 것을 확인할 수 있습니다.

