# Docker 실행시 permmision 오류 해결 방법

## 오류
### 예시

```bash
docker: permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock
```

### 원인

- 이 오류는 현재 사용자가 Docker 데몬 소켓 (`/var/run/docker.sock`)에 접근할 권한이 없기 때문에 발생합니다.


## 해결 방법

### 방법 1: Docker 그룹에 사용자 추가

Docker 그룹에 현재 사용자를 추가하여 권한 문제를 해결할 수 있습니다.

1. 현재 사용자를 Docker 그룹에 추가합니다.

```sh
sudo usermod -aG docker $USER
```

2. 그룹 변경 사항을 적용하기 위해 로그아웃하고 다시 로그인합니다. 또는 다음 명령어로 세션을 새로 고칩니다.

```sh
newgrp docker
```

### 방법 2: Docker 명령어를 `sudo`로 실행

Docker 명령어를 `sudo`로 실행하여 관리자 권한으로 실행할 수 있습니다. 예를 들어, 이미지를 가져오고 실행할 때 다음과 같이 명령어를 사용합니다.

```sh
sudo docker pull nginx
sudo docker run -d -p 80:80 --name mynginx nginx
```

### 방법 3: Docker 데몬이 실행 중인지 확인

Docker 데몬이 실행 중인지 확인하고, 실행 중이 아니라면 시작합니다.

1. Docker 데몬의 상태를 확인합니다.

```sh
sudo systemctl status docker
```

2. Docker 데몬이 실행 중이 아니라면 시작합니다.

```sh
sudo systemctl start docker
```

### 방법 4: Docker 설치 권한 수정

Docker 소켓의 권한을 수정하여 모든 사용자가 접근할 수 있도록 설정할 수도 있습니다. 그러나 이 방법은 보안상 권장되지 않습니다.

```sh
sudo chmod 666 /var/run/docker.sock
```

위의 방법 중 첫 번째 방법인 "Docker 그룹에 사용자 추가"를 사용하는 것이 가장 일반적이며 안전한 방법입니다. 이러한 방법을 시도하여 권한 문제를 해결하면 Docker 명령어를 정상적으로 실행할 수 있습니다.
