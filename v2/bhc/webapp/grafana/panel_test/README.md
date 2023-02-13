## Panel Test

### Table - hosts
Table panel을 테스트했습니다.<br>
ansible inventory에 등록된 hosts 정보를 출력합니다.

#### Query
```sql
select * from nodes;
```

#### Result
![](./img4doc/table_hosts.png)

### Time Series - Temperature
time series panel을 테스트했습니다.<br>
노드 별 시간 단위 온도 정보를 출력합니다.

#### Query
>쿼리 입력부 하단 ```Format as```를 Time series로 변경해야 합니다.<br>
>```Time formatted columns```에 시간 컬럼명을 태그로 추가해야 합니다.

```sql
select time, CAST(temperature as real), name from temp_convrt;
```

#### Result
![](./img4doc/time_temp.png)

### Gauge - Temperature
gauge panel을 테스트했습니다.<br>
현재 온도 정보를 게이지로 출력합니다.

#### Query
```sql
select CAST(temperature as real), name from temp_convrt where name = 'rpi6402' order by ROWID desc limit 1;
```

>쿼리를 노드 수만큼 추가해야 합니다. ```where name = '{node_name}'```

#### Result
![](./img4doc/gauge_temp.png)

### Time Series - CPU Usage
time series panel을 테스트했습니다.<br>
노드 별 시간 단위 cpu 사용률에 대한 정보를 출력합니다.

#### Query
>상기 time-temperature과 세팅은 동일합니다.

```sql
select time, 100-CAST(cpuratio as real), name from cpuinfo;
```

>사용률 정보는 idle status(유휴 상태)가 출력되기 때문에 100에서 idle percent를 빼줍니다.

#### Result
![](./img4doc/time_cpu.png)

### Pie Chart
pie chart panel 테스트했습니다.<br>
물리 디스크의 사용 중 용량, 잔여 용량 정보를 출력합니다.

#### Query
>Standard options tab에서 Unit에 단위를 추가할 수 있습니다.

```sql
select CAST(capacity as real) as capicty, CAST(inuse as real) as inuse, name from strginfo where name = 'rpi6402' order by ROWID desc limit 1;
```

#### Result
![](./img4doc/piechart_disk.png)

### Clock
clock panel을 테스트했습니다.<br>
현재 시간을 출력합니다.

#### Result
>별도의 쿼리가 없습니다.

![](./img4doc/clock.png)

### Time series - Memory Usage
time series panel을 활용한 메모리 사용률 정보 시각화입니다.<br>
난 노드의 메모리 사용률 변화를 출력합니다.

#### Query
```sql
select time, name, CAST(memratio as real) from meminfo;
```

#### Result
![](./img4doc/meminfo.png)

### Map - Location
map panel을 활용하여 노드의 위치 정보를 시각화합니다.<br>
한글 주소를 미리 입력받고 주소를 위도, 경도값으로 변환하여 지도에 해당 위치를 표시합니다. (python geopy)

#### Query
```sql
select CAST(latitude as real) as lat, CAST(longitude as real) as lng, name from location;
```

#### Result
![](./img4doc/location.png)

### Table - prediction
table panel을 활용해 모델이 추론한 결과를 시각화합니다.<br>
top5 추론 결과 중 최대값을 가지는 클래스만 호출합니다.

>추론 결과의 시각화 가능 여부 자체에 초점을 맞춘 작업입니다.<br>
>추론 결과 시각화 방안은 지속 고도화 중입니다.

#### Query
```sql
select name, class, max(probability) from modelpred;
```

#### Result
![](./img4doc/pred.png)

### Time series - Traffic
실시간 네트워크 트래픽량을 시각화합니다.<br>
vnstat module을 활용했습니다.

#### Query
```sql
select time, name, cast(tx_bps as real) from traffic;
select time, name, cast(rx_bps as real) from traffic;
```
tx : transmit data - 전송되는 데이터<br>
rx : receive data - 수신받는 데이터

#### result
![](./img4doc/time_traffic.png)
