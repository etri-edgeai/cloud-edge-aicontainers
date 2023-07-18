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


## EVC 환경 구성 및 요구사항
Edge vision Cluster 구동을 위한 환경을 구성합니다.<br>
EVC 구동을 위해 기본적으로 필요한 프레임워크, 패키지, 모듈을 설치합니다.


### Python && pip

conda 등 가상환경을 구성하는 것을 권장합니다.

* python version : 3.8.15
* schdule version : latest
* geopy version : latest

```bash
conda create -n evc python==3.8.15

pip install schedule
pip install geopy
```
> ```requirements.txt``` 참고

### Docker install
Private Registry Server 구축, AI model 리패키징 및 배포를 위해 Docker를 설치합니다.<br>

도커 설치 참고 : [Docker isntallation Guide](https://docs.docker.com/engine/install/ubuntu/)


### Ansible install
server, user node 간 통신 및 조작 | 제어를 위한 서버 관리 보조 어플리케이션 Ansible을 설치합니다.<br>

``` pip install ansible ```<br>


### Grafana install
클러스터 및 AI 모델 정보 시각화 관측을 위한 툴입니다. [Grafana Installation Guide](https://grafana.com/grafana/download)<br>

```bash
sudo apt-get install -y adduser libfontconfig1
wget https://dl.grafana.com/enterprise/release/grafana-enterprise_10.0.1_amd64.deb
sudo dpkg -i grafana-enterprise_10.0.1_amd64.deb
```


#### 대시보드 Export - Import
* Export
  grafana dashboard -> share click<br>
  export tab -> .json format download
* Import
  dashboard -> import tab<br>
  다운로드 받은 .json 파일 drag & drop


#### Datasource Permission 문제 해결
SQLite datasource 버전 업데이트 이후 권한 문제로 DB파일에 접근할 수 없는 문제 발생<br>
* config file 수정 적용 [sqlite datasource docs](https://github.com/fr-ser/grafana-sqlite-datasource/blob/main/docs/faq.md#i-have-a-permission-denied-error-for-my-database)<br>
  ```bash
  # edit (override) the grafana systemd configuration
  systemctl edit grafana-server
  
  # add the following lines
  [Service]
  ProtectHome=false
  
  # reload the systemd config and restart the app
  systemctl daemon-reload
  systemctl restart grafana-server
  ```


### Private Registry
AI 모델 이미지 저장, 관리 및 배포를 위한 사설 레지스트리 서버를 운영합니다.<br>
<br>
dockerhub에서 제공하는 기본 registry image를 사용합니다.<br>
<br>
```docker pull registry```<br>
<br>


#### Registry 접근 설정
* SSL 인증서 설정<br>
  <br>
  보안성 확립과 원활한 접근을 위해 SSL 사설 인증서로 관리합니다.<br>
  
  1. 인증서 생성 및 등록
     ```shell
     ## CA key, Certificate 생성
     mkdir certs && cd certs
     openssl genrsa -out rootca.key 2048
     openssl req -x509 -new -nodes -key rootca.key -days 365 -out rootca.crt

     ## extfile 생성
     echo subjectAltName = IP:123.214.186.252,IP:127.0.0.1 > extfile.cnf

     ## registry key, Private Certificate 생성
     openssl genrsa -out registry.key 2048
     openssl req -new -key registry.key -out registry.csr # Common NAME : 123.214.186.252 (registry ip)
     openssl x509 -req -in registry.csr -CA rootca.crt -CAkey rootca.key -CAcreateserial -out registry.crt -days 365 -extfile extfile.cnf

     ## 인증서 등록 및 docker 재실행
     cp registry.crt /usr/local/share/ca-certificates/registry.crt
     update-ca-certificates

     sudo systemctl restart docker
     ```

     >**SSL 설정을 원치 않을 경우**
     >* insecure-registry <br>
     >docker config file을 수정하여 http 프로토콜로 접근할 수 있습니다.<br>
     > ```shell
     > # 파일이 존재하지 않을 경우 생성
     > vi /etc/docker/daemon.json
     >  
     > # 내용 삽입 및 저장
     > {
     >    "insecure-registries" : ["localhost:5000"]
     > }
     > ```

  1. Reigstry Server Container 생성 <br>
     인증서가 저장된 디렉터리를 컨테이너에 마운트해야 합니다.<br>
     ```shell
     cd cloud-edge-aicontainers/v3/bhc/evc_frame
     sh registry_init.sh # 내부 내용 참고
     # 결과 확인
     docker ps -a # 컨테이너 생셩 여부
     curl https://localhost:5000/v2/_catalog -k # 컨테이너 응답 여부

     ## pull && push test
     docker pull python
     docker tag python localhost:5000/python
     docker push localhost:5000/python
     # 결과 확인
     curl https://localhost:5000/v2/_catalog -k
     curl https://localhost:5000/v2/python/tags/list -k
     ```
<br>
<br>


### Run EVC
EVC를 구동하여 모델 구축, 배포 및 모니터링 실행


#### 호스트 등록, 모델 구축 및 배포
```python runEVCv2.py```<br>

호스트 정보 등록과 저장, AI 모델 리패키징을 통한 docker image 생성 및 클러스터 배포를 일괄적으로 수행합니다.


#### 관측 및 모니터링
```python logger.py```<br>

각 클러스터의 다양한 상태 정보 및 AI 모델 관련 정보를 시각화하여 그라파나 서버로 송출합니다.


## EVC 설치 안내서
> EVC 설치 및 동작 테스트를 위한 절차 안내

### Backgrounds
하기 네 가지 요소가 충족되었다는 것을 전제 하에 진행됩니다.<br>

* python 기반 가상 환경
* docker
* ansible
* grafana

### EVC Tutorial
EVC 설치 시작
```bash
git clone git@github.com:againeureka/cloud-edge-aicontainers.git

## default path
# $PATH = $HOME/cloud-edge-aicontainers/v3/bhc/evc_frame/
```

1. Build Registry
   
   1-1. CA certificate 등록
   
        ```bash
        pwd
        ## > /home/{my_account}
        
        ## CA key, Certificate 생성
        mkdir certs && cd certs
        openssl genrsa -out rootca.key 2048
        openssl req -x509 -new -nodes -key rootca.key -days 365 -out rootca.crt
        
        ## extfile 생성
        echo subjectAltName = IP:{my_ip},IP:127.0.0.1 > extfile.cnf  # my_ip : 공인 아이피 주소 (외부 접속 주소)
        
        ## registry key, Private Certificate 생성
        openssl genrsa -out registry.key 2048
        openssl req -new -key registry.key -out registry.csr
        openssl x509 -req -in registry.csr -CA rootca.crt -CAkey rootca.key -CAcreateserial -out registry.crt -days 365 -extfile extfile.cnf
        
        ## 인증서 등록 및 docker 재실행
        sudo cp registry.crt /usr/local/share/ca-certificates/registry.crt
        sudo update-ca-certificates
        
        sudo systemctl restart docker
        ```

    1-2. Registry 컨테이너 생성
   
         ```bash
         ## pull from dockerhub
         docker pull registry
         
         ## get list
         docker images
         
         ## run registry container
         cd cloud-edge-aicontainers/v3/bhc/evc_frame
         
         vi registry_init.sh
         # 인증서 마운트 디렉터리 수정
         
         sh registry_init.sh
         
         ## get containers list
         docker ps -a
         
         ### registry test
         ## connection test
         curl https://localhost:5000/v2/_catalog -k
         
         ## pull & push test
         # pull random image from dockerhub
         docker pull python
         # rename image
         docker tag python localhost:5000/python
         # push to the registry
         docker push localhost:5000/python
         # get list
         curl https://localhost:5000/v2/_catalog -k
         curl https://localhost:5000/v2/python/tags/list
         ```
         >포트 포워딩 설정 후 외부로부터 접속 가능

2. Database initialize (optional)

   EVC github 프로젝트는 edge_logs.db3 파일을 포함하고 있습니다.<br>
   필요에 따라 새로운 DB를 생성하여 초기화할 수 있습니다.<br>
   SQLite3 DB를 사용합니다.<br>

   ```bash
   cd $PATH/db/
   
   ## 기존 db 삭제
   rm edge_logs.db3

   ## 빈 db 파일 생성
   python init_db.py
   ```


3. set Grafana Dashboard

   dashboard.json 다운로드 위치 : ```$PATH/dashboards/grafana/```

   3-1. Import dashboards
   
   * 그라파나 접속<br>
     ```http://localhost:3000/  # default port 3000``` 
   * 대시보드 JSON model import 기능을 사용하여 대시보드 업데이트 <br>
     ```Dashboards -> New -> Import  # .json 파일 drag & drop```

   3-2. Datasource 연결
   
   * Plugin 설치 <br>
     ```Administration -> Plugins (state : all) -> SQLite plugin 검색 및 설치```
   * Datasource 생성 및 적용 <br>
     ```Connections -> Datasource -> Add new datasource -> db파일 경로 입력 및 저장```

   * (Optional) Permission error 해결
  
     간헐적으로 Grafana 계정의 권한 문제로 DB 파일에 접근할 수 없는 문제가 발생합니다.<br>
     
     ```bash
     # edit (override) the grafana systemd configuration
     systemctl edit grafana-server
     
     # add the following lines
     [Service]
     ProtectHome=false
     
     # reload the systemd config and restart the app
     systemctl daemon-reload
     systemctl restart grafana-server
     ```


4. Run EVC

    EVC를 구동합니다. 하기 절차를 수행합니다.<br>
    
    * download user project
    * edge hosts config
    * model repackage
    * model deploy
    * model run<br>
    <br>

    ```bash
    cd $PATH/EVC_RunTest
    python runEVCv2.py
    ```

5. Monitor

   엣지 클러스터를 모니터링합니다.

   ```bash
   cd $PATH/db

   python logger.py
   ```
