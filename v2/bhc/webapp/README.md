# 웹 애플리케이션 프레임워크 제작
Edge Container 제작, 배포 및 모니터링 기능을 수행할 수 있는 Edge Framework를 개발합니다.<br>

## 기능, 요소
- 모델 이미지 빌드
  - 빌드 과정 모니터
  
- 레지스트리에 이미지 등록
  - 레지스트리 목록 출력
  
- 엣지 노드에 이미지 배포
  - 신규 노드 등록 기능
  - 보유 노드 목록 출력
    - 위치 정보
    - 시스템 정보
    - 상태 정보 (ex. 온도)

- 컨테이너 구축

- 모델 추론 수행
  - 추론 결과 모니터
  - 사용중인 모델 정보
  
- Database 구축
  - 로그 수집 및 저장

- 시각화
  - 로그 데이터를 연동을 통한 시각화

## ```Grafana```
데이터 시각화 웹 어플리케이션

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

### Pannel Test
Table pannel을 테스트했습니다.<br>
![](./img4doc/table.png)

## ```DB```
SQLite를 사용하여 데이터베이스를 구축했습니다.<br>
```SQL
create table nodes;

insert into nodes (id, name, ip)
values (01, 'rpi6401', 'keti@192.168.1.241');
```
