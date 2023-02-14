# 개별 노드 모니터링
개별 노드에 대한 정보를 선택적으로 조회할 수 있습니다.<br>
네트워크 상태와 모델에 대한 정보를 조회하여 배포 과정을 시각적으로 확인할 수 있습니다.<br>

> 기존 ```admin_monitor```대시보드에 구현되어 있는 내용은 생략합니다.

## traffic
노드의 네트워크 트래픽의 변화 추이를 관측합니다.<br>
<br>
모델 배포 시 변화하는 트래픽을 감지하여 배포가 정상 수행 중임을 확인할 수 있습니다.<br>
트래픽 조회를 위한 커맨드를 사용합니다.<br>
```bash
vnstat -tr 10 --json
```

- **rx_bps**<br>
  received packets ( 단위 : byte_per_sec )

- **tx_bps**<br>
  transmitted packets ( 단위 : byte_per_sec )


## model list
레지스트리 서버에 등록된 모델 목록을 조회합니다.<br>
<br>
조회를 위한 커맨드를 사용합니다.<br>
```bash
curl -s https://{registry}/v2/_catalog -k

curl -s https://{registry}/v2/{data}/tags/list -k
```

- **name**<br>
  AI model의 이름입니다.<br>
  작명의 기준은 "빌드된 CPU Architecture" 입니다.(변경될 수 있습니다.)

- **tag**<br>
  model image의 태그 정보입니다.<br>
  작명의 기준은 "수행하는 태스크" | "학습한 데이터셋" 입니다.(변경될 수 있습니다.)

## model description
배포 절차 수행 시 배포하는 모델에 대한 설명을 출력합니다.<br>
<br>
python docstring으로 수기 저장되어 있으며 모델 이름, 태그 정보를 통해 원하는 desc를 반환합니다.<br>

- **desc**<br>
  모델에 대한 개괄적인 설명<br>
  수기 작성

## progress
모델 배포 수행 시 과정의 상태 정보를 출력합니다.<br>
<br>
event alert 기능을 수행하는 패널입니다.<br>

- **status**<br>
  배포 상태에 대한 정보입니다.<br>
  <br>
  두 가지 값을 가집니다.<br>
  - activating
  - done

