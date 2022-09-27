# docker

## docker permission 문제 해결

- 출처 : https://stackoverflow.com/questions/48957195/how-to-fix-docker-got-permission-denied-issue

1. docker 그룹을 생성합니다 (Create the docker group if it does not exist)
```bash
$ sudo groupadd docker
```

2. 사용자 계정을 docker group에 추가합니다 (Add your user to the docker group.)
```bash
$ sudo usermod -aG docker $USER
```

3. Run the following command or Logout and login again and run (that doesn't work you may need to reboot your machine first)
$ newgrp docker

Check if docker can be run without root
$ docker run hello-world
Reboot if still got error

$ reboot