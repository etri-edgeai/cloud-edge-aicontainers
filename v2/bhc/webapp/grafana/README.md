# Grafana : 시각화 웹 애플리케이션 구축
data source를 연결하여 다양한 대시보드를 통해 시각화하는 툴입니다.<br>
구축한 데이터베이스 파일을 연결하여 데이터 포맷과 수집 목적에 맞는 방식으로 시각화하고 분석하는 방안을 제시합니다.<br>
자체 프레임워크 제작을 위한 환경 구성에 대한 내용을 포함합니다.

## Grafana Tutorial

### installation
ubuntu 20.04 기준 설치 방법입니다<br>
```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y apt-transport-https
sudo apt-get install -y software-properties-common wget
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
sudo apt-get update
sudo apt-get install grafana
```

### start grafana
```bash
sudo service grafana-server start
```
3000번 포트로 연결됩니다.<br>
>**Default 계정**
>- username : admin
>- password : admin

### Panel Test
각 패널의 기능과 사용법을 테스트합니다.<br>
> 상세 내용을 ```panel_test```에 기재합니다.<br>

## Dashboards
엣지 노드와 모델을 관리, 모니터링하기 위한 대시보드를 구축합니다.<br>
각 대시보드의 동적인 상호 작용과 실행, 사용자화 등을 위한 고도화 방안을 포함합니다.<br>

### admin_monitor
각 노드의 다양한 상태 정보를 관측할 수 있는 관리자 모니터링 대시보드입니다.<br>
아래 내용을 포함합니다.<br>
- 관리 중인 노드 목록
- 각 노드의 위치 정보
- 각 노드의 잔여 용량
- 각 노드의 cpu 온도
- 각 노드의 온도 변화 추이
- 각 노드의 cpu 사용량 변화 추이
- 각 노드의 memory 사용량 변화 추이
> 상세 내용을 ```admin_monitor```에 기재합니다.<br>

### single_node_monitor
개별 노드의 다양한 상태 정보를 관측하고, 모델의 배포 과정을 관측하기 위한 대시보드를 구축합니다.<br>
아래 내용을 포함합니다.<br>
- 용량 정보
- 온도
- 메모리 사용량
- cpu 사용량
- 레지스트리 서버에 등록된 모델 정보
- 네트워크 트래픽
- 배포한 모델에 대한 설명
- 모델 배포 상태 알림창
> 상세 내용을 ```single_node_monitor```에 기재합니다.<br>


### inference_monitor
노드 내 모델 컨테이너가 수행한 추론 정보에 대한 시각화를 위한 대시보드를 구축합니다.<br>
아래 내용을 포함합니다.<br>
- 추론 대상 데이터 (이미지, 텍스트, etc.)
- 추론 결과값
> 상세 내용을 ```inference_monitor```에 기재합니다.<br>
