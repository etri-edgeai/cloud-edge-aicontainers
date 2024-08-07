# Install Docker


## On Raspberry Pi 4 and 5

Raspberry Pi 4 or 5에서 64비트 OS를 설치하고 Docker를 설치하는 방법을 단계별로 설명합니다.

### 1. 64비트 OS 설치

Raspberry Pi 4 or 5에 64비트 OS를 설치하기 위해 공식 Raspberry Pi OS를 사용하겠습니다. 다음 단계에 따라 설치를 진행합니다.

#### a. Raspberry Pi Imager 다운로드 및 설치
Raspberry Pi Imager를 다운로드하고 설치합니다. Raspberry Pi Imager는 공식 웹사이트에서 다운로드할 수 있습니다.

[Raspberry Pi Imager 다운로드](https://www.raspberrypi.org/software/)

#### b. SD 카드 준비
Raspberry Pi에 사용할 SD 카드를 준비합니다. 최소 16GB 이상의 SD 카드를 권장합니다.

#### c. 64비트 Raspberry Pi OS 설치
1. Raspberry Pi Imager를 실행합니다.
2. "Choose OS"를 클릭합니다.
3. "Raspberry Pi OS (other)"를 선택합니다.
4. "Raspberry Pi OS (64-bit)"를 선택합니다.
5. "Choose SD Card"를 클릭하여 SD 카드를 선택합니다.
6. "Write"를 클릭하여 64비트 OS를 SD 카드에 씁니다.

### 2. Docker 설치

Raspberry Pi OS에서 Docker를 설치하는 방법을 설명합니다. Raspberry Pi의 터미널에서 다음 명령어를 실행합니다.

#### a. 시스템 업데이트
먼저 시스템을 업데이트합니다.

```bash
sudo apt update
sudo apt upgrade -y
```

#### b. Docker 설치
Docker의 설치 스크립트를 실행하여 Docker를 설치합니다.

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

#### c. Docker 사용자 그룹 설정
현재 사용자를 Docker 그룹에 추가하여 sudo 없이 Docker 명령어를 사용할 수 있도록 설정합니다.

```bash
sudo usermod -aG docker $USER
```

#### d. 변경사항 적용
사용자를 Docker 그룹에 추가한 후, 변경사항을 적용하기 위해 로그아웃하고 다시 로그인합니다. 또는 다음 명령어를 실행하여 세션을 새로 고칩니다.

```bash
newgrp docker
```

### 3. Docker 설치 확인
Docker가 올바르게 설치되었는지 확인합니다.

```bash
docker --version
```

정상적으로 설치되었다면 Docker 버전 정보가 출력됩니다.

```bash
docker run hello-world
```

이 명령어를 실행하면 Docker가 정상적으로 작동하는지 테스트하는 메시지가 출력됩니다.

### 요약
1. Raspberry Pi Imager를 사용하여 64비트 Raspberry Pi OS를 SD 카드에 설치합니다.
2. Raspberry Pi에 SD 카드를 삽입하고 부팅합니다.
3. 터미널을 열고 시스템을 업데이트합니다.
4. Docker 설치 스크립트를 실행하여 Docker를 설치합니다.
5. 현재 사용자를 Docker 그룹에 추가합니다.
6. Docker 설치를 확인하고 테스트합니다.

이 단계를 따르면 Raspberry Pi 5에서 64비트 OS와 Docker를 성공적으로 설치할 수 있습니다.
