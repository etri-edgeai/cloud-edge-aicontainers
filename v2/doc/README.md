# 개념 정의


## 요구사항(Requirement)
- 기능 요구사항 (Functional Requirement)

  . 시스템의 기능으로서 요구되는 사항입니다.
  . 시스템이나 소프트웨어가 할 수 있는 일을 정의합니다.

- 비기능 요구사항 (Non-functional requirement)

  . 시스템의 {성능, 신뢰성, 확장성, 운용성, 보안성능}과 같이 기능을 제외한 요구사항들을 의미합니다.

## Approach

- Docker container based micro architecture service


# 임시
----------------------

# apache_install

http://ketiabcs.iptime.org:39180/


## ubuntu에 apache2 웹서버 설치

- https://askforyou.tistory.com/120

```bash
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install apache2
sudo service apache2 status

sudo service apache2 start
sudo service apache2 stop


```

## default directory
/var/www/html/index.html  


## change default home directory

```bash
cd /etc/apache2/sites-available

vi 000-default.conf

# DocumentRoot /var/www/html 희망 경로로 수정

cd /etc/apache2/
vim apache2.conf

# directory /var/www/html 희망 경로로 수정

service apache2 restart

```


## 기존 사용자 그룹에 추가

- (사용법) sudo usermod -a -G groupname username

sudo usermod -a -G apache jpark


## 아파치 쓰기 권한 부여
- (참고) https://devlog.jwgo.kr/2017/01/03/aws-apache-websvr-permissions/


ps -ef | egrep 'httpd|apache2'


