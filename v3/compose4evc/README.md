# 개발을 위한 리눅스 명령어

### 네트워크

#### 포트 확인

- sudo 권한으로 실행해야 프로그램 이름까지 확인 가능

```bash
sudo netstat -aNp | grep 9090
```

### 서비스

#### 서비스 확인

```bash
sudo service  --status-all
```

### 기타 응용프로그램

#### 깃랩

- 설정 파일 수정

```bash
sudo vi /etc/gitlab/gitlab.rb
```
- 재시작

```bash
$ sudo gitlab-ctl reconfigure
$ sudo gitlab-rake gitlab:check
$ sudo gitlab-ctl status
```

- 그라파나 비활성화

```bash
$ vi /etc/gitlab/gitlab.rb
  grafana['enable'] = false

$ sudo gitlab-ctl reconfigure
$ sudo gitlab-rake gitlab:check
$ sudo gitlab-ctl status
```


- 프로메테우스 비활성화

```bash
$ vi /etc/gitlab/gitlab.rb
  prometheus_monitoring['enable'] = false

$ sudo gitlab-ctl reconfigure
$ sudo gitlab-rake gitlab:check
$ sudo gitlab-ctl status
```

- gitlab 번들 nginx 비활성화

```bash
$ vi /etc/gitlab/gitlab.rb
  nginx['enable'] = false
  
$ sudo gitlab-ctl reconfigure
$ sudo gitlab-rake gitlab:check
$ sudo gitlab-ctl status

```
### 그라파나 데시보드 + docker-compose

- https://bobocomi.tistory.com/103

### 앤서블 세마포어

- 중요 참고문서 : https://www.ansible-semaphore.com/blog/installation-and-removal/


```bash
Connect to the server where Semaphore will run
$ ssh user123@server456

Switch to root user
$ sudo -s

Update packages
$ apt update

Install snap
$ apt install snapd

Install Semaphore using snap
$ snap install semaphore

Stop Semaphore service, it is required to manage Semaphore via CLI
$ snap stop semaphore

Add admin user
$ semaphore user add --admin --login admin --name Admin --email admin@example.com --password 123456

Start Semaphore service
$ snap start semaphore

Open Semaphore UI in browser by address 
http://server456:3000

```


## docker-compose 에서 사용자 접근 권한 문제

- https://github.com/prometheus/prometheus/issues/5976

## 도커

### 도커 컨테이너에 쉘로 접속하기

```bash
docker exec -it e112cba194f3 /bin/bash
```