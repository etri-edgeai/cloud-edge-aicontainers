# API

- 참고 : https://github.com/shahbaz17/php-rest-api
- 수정 : JPark, 2023

## 참고

### apache2 삭제

```bash
$ service --status-all
...
[ + ]  apache-htcacheclean
[ + ]  apache2
...

; 아파치 웹서버 삭제
$ service apache2 stop
$ apt-get remove apache2*
$ apt-get --purge remove apache2*
$ apt-get autoremove

sudo apt purge  apache2*


; 아파치 웹서버 캐시 클리닝 대몬 삭제
$ service apache-htcacheclean stop
$ apt-get remove apache*
$ apt-get --purge remove apache*
$ apt-get autoremove

; 마지막으로 OS를 최신상태로
$ apt update
$ apt upgrade
```

### nginx 삭제

```bash
sudo apt-get remove --purge nginx nginx-full nginx-common 
```

### 포트 상태 확인

```bash
netstat -anot | grep :80
```
-a :  모든 port를 나타내는 옵션
-n : IP주소뒤에 port 번호까지 보여주는 옵션
-o : PID(프로세스ID) 를 보여주는 옵션

### 서비스 목록

```bash
service --status-all
```

### 특정 포트 프로세스 제거

sudo lsof -i :80
sudo fuser -n tcp -k 80


### nginx docker 빌드 및 실행

docker run -d -p 81:80 -v /home/jpark/www/cloud-edge-aicontainers/v3:/usr/share/nginx/html localhost:5000/evc-nginx

docker run -d -p 81:80 -v /home/jpark/www/cloud-edge-aicontainers/v3:/var/www/html localhost:5000/evc-nginx





docker run -d --name nginx_mount -p 5555:80 -v /root/webdata:/usr/share/nginx/html:ro nginx


### docker-compose 명령어

https://www.daleseo.com/docker-compose/







## Build a Simple REST API in PHP

This example shows how to build a simple REST API in core PHP.

Please read https://dev.to/shahbaz17/build-a-simple-rest-api-in-php-2edl to learn more about REST API.

### Prerequisites

- [PHP](https://www.php.net/downloads.php)
- [MySQL](https://www.mysql.com/downloads/)
- [Composer](http://getcomposer.org/)
- [Postman](https://www.postman.com/downloads/)

## Getting Started

Clone this project with the following commands:

```bash
git clone https://github.com/shahbaz17/php-rest-api.git
cd php-rest-api
```

### Configure the application

Create the database and user for the project.

```php
mysql -u root -p
CREATE DATABASE blog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'rest_api_user'@'localhost' identified by 'rest_api_password';
GRANT ALL on blog.* to 'rest_api_user'@'localhost';
quit
```

Create the `post` table.

```php
mysql -u rest_api_user -p;
// Enter your password
use blog;

CREATE TABLE `post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `body` text NOT NULL,
  `author` varchar(255),
  `author_picture` varchar(255),
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);
```

Copy `.env.example` to `.env` file and enter your database deatils.

```bash
cp .env.example .env
```

## Development

Install the project dependencies and start the PHP server:

```bash
composer install
```

```bash
php -S localhost:8000 -t api
```

## Your APIs

| API               |    CRUD    |                                Description |
| :---------------- | :--------: | -----------------------------------------: |
| GET /posts        |  **READ**  |        Get all the Posts from `post` table |
| GET /post/{id}    |  **READ**  |        Get a single Post from `post` table |
| POST /post        | **CREATE** | Create a Post and insert into `post` table |
| PUT /post/{id}    | **UPDATE** |            Update the Post in `post` table |
| DELETE /post/{id} | **DELETE** |            Delete a Post from `post` table |

Test the API endpoints using [Postman](https://www.postman.com/).

## License

See [License](./LICENSE)