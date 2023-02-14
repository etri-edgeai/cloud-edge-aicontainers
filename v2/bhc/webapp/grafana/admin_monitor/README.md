# 관리자 모니터링 대시보드 
서버에 등록된 모든 노드에 대한 다양한 정보를 관측할 수 있는 대시보드입니다.<br>

## node list
서버에 등록된 노드의 목록을 보여줍니다.<br>
<br>
table panel로 구현되었습니다.<br>
<br>
ansible hosts file 로부터 정보를 가져옵니다.<br>

- **id**<br>
  노드의 고유값<br>
  일차적으로 무작위 정수값으로 구현되었습니다. ```randint()```<br>
  추후 각 노드의 로그인 등 추가 기능을 위한 primary key로 사용될 수 있습니다.
  
- **name**<br>
  각 노드의 이름입니다.<br>
  host_name을 사용했습니다.<br>
  ansible 명령 전달 시 host 구분을 위해 사용합니다.<br>

- **type**<br>
  노드의 사용 목적입니다.<br>
  
  - builder : 해당 노드에 맞는 모델 이미지를 빌드하기 위해 사용되는 노드입니다.<br>
  
  - user : 모델을 다운로드받아 사용하는 노드입니다.<br>
  
## location
등록된 노드의 위치 정보를 보여줍니다.<br>
<br>
geomap panel로 구현되었습니다.<br>
<br>
geocoding을 사용하여 한글 주소를 위, 경도값으로 정제하여 읽어오는 방식으로 현재 위치 정보를 획득합니다.<br>

- **lat**<br>
  위도값입니다.<br>
- **lng**<br>
  경도값입니다.<br>
- **name**<br>
  노드의 이름입니다.<br>

## storage
노드의 잔여 용량 정보를 보여줍니다.<br>
<br>
pie chart panel로 구현되었습니다.<br>
<br>
용량 정보를 가져오기 위한 커맨드를 사용합니다.<br>
```bash
## 총용량
df -P | grep -v ^Filesystem | awk '{sum += $2} END {print sum/1024/1024}'
# $3, $4 로 변경하여 각각 inuse, capacity 획득
```
<br>
지속적으로 용량 정보를 기록하고 마지막 데이터만 호출합니다. ```order by ROWID desc limit 1```

- **capacity**<br>
  사용 가능한 용량 (단위 : gb)<br>

- **inuse**<br>
  사용된 용량 (단위 : gb)<br>

- **name**<br>

## temperature
노드의 온도 정보( cpu 온도 )를 보여줍니다.<br>
<br>
gauge, time series 두 가지 방식으로 구현되었습니다.<br>
<br>
온도 정보를 가져오기 위해 커맨드를 사용합니다.<br>
```bash
cat /sys/devices/virtual/thermal/thermal_zone0/temp
# 노드에 따라 디렉터리가 변경될 수 있습니다.
```
> 중복되는 컬럼 정보는 생략합니다.

- **time**<br>
  기록 당시 시간<br>
- **name**<br>
  노드 이름<br>
- **temperature**<br>
  온도 정보 (단위 : celsius)

### current temperature
현재 온도값입니다.<br>
온도 정보 데이터에서 최신 데이터만 호출합니다.<br>
gauge panel로 구현되었습니다.<br>

### node temperature
노드 별 온도 변화 추이입니다.<br>
time series panel로 구현되었습니다.<br>

## memory usage
노드 별 메모리 사용량 변화 추이입니다.<br>
<br>
time series panel로 구현되었습니다.<br>
<br>
메모리 사용량 정보 호출을 위한 커맨드를 사용합니다.<br>
```bash
cat /proc/meminfo | grep Mem
```

- **memratio**<br>
  사용 중인 메모리 비율<br>

## cpu usage
노드 별 cpu 사용률 변화 추이입니다.<br>
<br>
time series panel로 구현되었습니다.<br>
<br>
cpu 사용량 정보 호출을 위한 커맨드를 사용합니다.<br>
```bash
top -b -n 1 | grep -Po '[0-9.]+ id'
```

- **cpuratio**<br>
  잔여 cpu 사용률<br>
