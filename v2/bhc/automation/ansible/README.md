## Ansible 네트워크 구성
ansible을 활용한 통신 네트워크 구성을 통해 작업 편의성 확보 및 원격 조작을 수행합니다.<br>

### 용도 및 기능
- builder nodes의 dockerfile image build -> push 절차 원격 구동
- user nodes의 image pull -> run & exec container 절차 원격 구동
- 실험 및 작업 간 편의성 확보
- 인증 절차 간소화

### 사전 작업
비대칭기 암호화 기술을 활용해 노드 간 인증 절차를 생략합니다.<br>
공개키 - 개인키 쌍을 생성한 뒤 접근하고자 하는 노드에 공개키를 보냅니다.<br>

```bash
## RSA 암호 알고리즘 사용
$ ssh-keygen -t rsa

## 공개키 송부
$ ssh-copy-id keti@192.168.1.241

## access test
ssh keti@192.168.1.241
```

구성이 완료되면 암호를 묻지 않고 접속됩니다.

### init ansible

#### download

```bash
$ pip isntall ansible==2.10.7
$ ansible --version
```

#### set hosts

```bash
$ cd /etc
$ mkdir ansible
$ vi hosts
```

hosts 파일 작성

```bash
[builders]
  rpi6401 keti@192.168.1.241
  rpi6402 keti@192.168.1.242

:w !sudo tee % > /dev/null
:q!
```

테스트 수행<br>
```$ ansible builders -m ping```

#### sending files | directories

```bash
$ vi copy.yaml
$ ansible-playbook copy.yaml
```

### test
ansible 명령 전달 및 수행 여부를 테스트합니다.<br>
필요한 절차에 대한 playbook을 작성하여 자동화하는 작업을 수행합니다. 테스트 과정에서 필요한 기능을 찾아 고도화합니다.

### copy.yaml
모델 이미지 구축을 시작하기 전 구축에 필요한 Dockerfile 스크립트와 model.tar.gz 압축파일을 전송하기 위한 playbook입니다.<br>
model 압축파일은 모델 파이썬 파일과 학습 가중치 파일, 테스트 데이터와 requirements.txt 패키지 목록을 포함합니다.

### autorun.yaml
테스트 과정을 마친 스크립트를 하나의 playbook으로 작성하였습니다.<br>
cpu-arch detection -> build image -> model test -> push image 의 절차를 일괄적으로 수행합니다.<br>
- **cpu architecture detection :** 모델 배포 시 해당 노드 구분을 위해 cpu 기반 구조를 탐지하여 기록합니다.
- **build image :** rule set 에 따라 정해진 이름의 docker image를 구축합니다.
- **model test :** 구축된 이미지로 컨테이너를 생성하고 모델 정상 작동 여부를 테스트합니다.
- **push image :** 테스트가 완료된 이미지를 레지스트리에 업로드합니다.

