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

### copy.yaml

### autorun.yaml
