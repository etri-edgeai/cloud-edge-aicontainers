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


## 기능

### 모델 배포
- 모델 이미지 빌드
- 레지스트리 등록
- 대상 노드에 이미지 배포, 컨테이너 생성
>진행 상황, 네트워크 상태, 배포 결과 등에 대한 모니터링 수행
  
### 추론 수행
- 대상 노드 원격 제어를 통한 추론 수행
- 추론 결과 시각화
>시나리오 기반으로 결과를 모니터합니다. (Grafana를 통한 시각화)<br>
>- Re-ID
>- Smart Farm
>- etc..
  
### 엣지 노드 모니터링
- 등록된 노드에 대한 로그 수집
- 로그 데이터 시각화
>Grafana를 활용하여 데이터를 시각화합니다. 다양한 정보(```db/``` 참조)를 포함합니다.



## ```Grafana```
**데이터 시각화 웹 어플리케이션**<br>
<br>
> 저장된 데이터를 적절한 대시보드와 연결하여 사용자, 혹은 관리자가 편리하게 조회할 수 있도록 돕는 프레임워크입니다.<br>
초기 설치와 기초적인 사용 방법, 나아가 데이터 구축에 따른 고도화, 자체 프레임워크 제작을 위한 환경 구성 등의 내용을 포함합니다.<br>

상세 내용을 ```grafana/``` 내부에 기재합니다.



## ```DB```
**로그 등 필요 데이터 수집 및 정리**<br>
<br>
> 노드 정보, 추론 정보, 시스템 정보 등을 조회하기 위해 로그 형태 등으로 데이터화하여 수집, 보관합니다.<br>
저장한 데이터를 토대로 grafana에 연결하여 시각화하는 용도로 또한 사용할 수 있습니다.<br>
DB 구축, 데이터 조작 및 전처리 등 작업을 모두 포함합니다.<br>

상세 내용을 ```db/``` 내부에 기재합니다.



## ```playbooks```
**각 노드에 필요한 명령을 전달하기 위한 스크립트**<br>
<br>
> 네트워크에 등록된 노드들에게 필요한 명령어를 전달하기 위해 구성된 ansible-playbook script입니다.<br>
> 레지스트리 서버 CA 인증서 복사, AI 모델 소스코드 복사, 도커 이미지 빌드 및 배포, AI 모델 런 등을 수행합니다.<br>

**각 파일 경로**
* ```copy_cert.yaml``` : 레지스트리 서버 접속을 위해 인증서를 원격지 노드에 복사합니다.
* ```del_cert.yaml``` : 노드 삭제 시 레지스트리 접속 차단을 위해 인증서 정보를 삭제합니다.
* ```db/model/run_model.yaml``` : 원격지 노드에 AI 모델 컨테이너를 생성하고 추론을 수행합니다.
* ```db/model/img_build/autorun.yaml``` : 배포용 AI 모델 구축을 위한 통합 플레이북입니다.
* ```db/model/img_build/copy_model.yaml``` : AI 모델의 소스코드를 builder node에 복사합니다.
* ```db/run_playbook.yaml``` : DB에 기록하기 위한 각종 로그를 생성합니다.


## ```Interface```
**기능 동작 명령을 전달하기 위한 인터페이스 생성**<br>
<br>
> 구현된 기능을 관리자 혹은 사용자가 사용할 수 있어야 합니다.<br>
> 기능을 목적에 맞게 절차적으로 연결하고 통합적으로 수행할 수 있어야 합니다.<br>
> FastAPI 등을 활용하여 원격에서 명령을 수행할 수 있도록 고도화할 예정입니다.<br>

### ```m_device.py```
원격지의 엣지 노드를 통제하기 위한 기능을 수행하기 위한 인터페이스입니다.<br>
>콘솔에서 작동하며, argumentparser로 인자를 전달받아 명령을 수행합니다.<br>
>노드 등록, 삭제, 조회, DB 저장 등을 수행합니다.<br>
>
>#### ```run_devicemanager.sh```
>노드 제어 인터페이스를 동작하기 위한 예시 스크립트입니다.
>
>#### ```hosts.ini```
>노드 등록/삭제 시 변경 내용을 적용하여 생성되는 ansible-inventory(hosts configuration file)입니다.

### ```m_model.py```
AI 모델을 조작하는 기능을 수행하기 위한 인터페이스입니다.
>콘솔에서 작동하며, argumentparser로 인자를 전달받아 명령을 수행합니다.<br>
>배포용 AI 모델 이미지 구축, 레지스트리에 이미지 등록/삭제, AI 모델 배포, 컨테이너 생성, 추론 수행, DB 저장 등을 수행합니다.<br>
>
>#### ```run_modelmanager.sh```
>AI 모델 제어 인터페이스를 동작하기 위한 예시 스크립트입니다.


## ```Configuration file Based EVC Activation```
**동작 구성을 정의한 파일을 사용한 EVC 구동 방안**<br>
<br>
> yaml 포맷을 사용하여 동작을 정의합니다.<br>
> EVC는 yaml 파일 내 데이터를 파싱하여 task를 실행합니다.<br>
> 사용자가 구성 파일을 사용할 수 있도록 guidance를 제공합니다.<br>

상세 내용을 ```run_cfg/``` 내부에 기재합니다.
