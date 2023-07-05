# Edge Vision Cluster
분산 환경 디바이스 관측, 관리 및 클러스터링과 기계학습 지원을 수행하기 위한 프레임워크입니다.<br>

## 구성

```
evc_frame
│
├── registry_init.sh
│
├── m_device.py
├── m_model.py
│
├── EVC_RunTest
│   ├── ServerConfig.yaml
│   ├── get_prj.py
│   ├── hosts.ini
│   └── runEVCv2.py
│
├── db
│   ├── edge_logs.db3
│   ├── init_db.py
│   └── logger.py
│       ├── get_geoloc_db.py
│       ├── hosts.py
│       ├── get_model.py
│       ├── run_model.py
│       ├── get_network_db.py
│       ├── get_sysinfo_db.py
│       └── get_temp_db.py
│
└── playbooks
    ├── autorun.yaml
    ├── copy_cert.yaml
    ├── copy_model.yaml
    ├── get_logs.yaml
    └── run_model.yaml

```


## Get start with EVC
Edge vision Cluster 구동을 위한 환경을 구성합니다.

### Environment Settings
EVC 구동을 위해 기본적으로 필요한 프레임워크, 패키지, 모듈을 설치합니다.

* python version : 3.8.15

#### Docker install
Private Registry Server 구축, AI model 리패키징 및 배포를 위해 Docker를 설치합니다.<br>

도커 설치 참고 : [Docker isntallation Guidance](https://docs.docker.com/engine/install/ubuntu/)

#### Ansible install
server, user node 간 통신 및 조작 | 제어를 위한 서버 관리 보조 어플리케이션 Ansible을 설치합니다.<br>

``` pip install ansible ```

#### Package installation
기타 필요한 패키지를 설치합니다.<br>
<br>
사용된 주요 패키지는 다음과 같습니다.
* geopy
* pytorch
* ultralytics

```requirements.txt``` 참고


#### Build Private Registry
AI 모델 이미지 저장, 관리 및 배포를 위한 사설 레지스트리 서버를 운영합니다.<br>
<br>
dockerhub에서 제공하는 기본 registry image를 사용합니다.<br>
<br>
```docker pull registry```<br>
<br>
##### registry 접근 설정

* SSL 인증서 설정
보안성 확립과 원활한 접근을 위해 SSL 사설 인증서로 관리합니다.<br>
<br>
<br>

* insecure-registry <br>
SSL 인증서 설정을 원치 않을 경우 config file을 수정하여 http 프로토콜로 접근할 수 있습니다.<br>
```shell
# 파일이 존재하지 않을 경우 생성
vi /etc/docker/daemon.json

# 내용 삽입 및 저장
{
   "insecure-registries" : ["localhost:5000"]
}
```
<br>


업데이트 중
