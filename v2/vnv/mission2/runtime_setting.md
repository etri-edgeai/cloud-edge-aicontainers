# runtime setting 

## Ubuntu 20.04 LTS + CUDA 11.7 + pytorch 1.12.1

### (1) download, cuda_11.7.1_515.65.01_linux.run


- update
```bash
$ sudo apt update && sudo apt upgrade -y
```

- search 1
```bash
$ ubuntu-drivers devices
```

- search 2 (최신버전 설치)
```bash
apt search nvidia-driver
```

- install

```bash
$ sudo apt install nvidia-driver-515
```


- reboot

```bash
$ sudo reboot
```

- test

```bash
$ nvidia-smi
```

- 

```bash
$ https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=20.04&target_type=runfile_local
```

- data

```bash
$ wget https://developer.download.nvidia.com/compute/cuda/11.7.1/local_installers/cuda_11.7.1_515.65.01_linux.run

$ sudo sh cuda_11.7.1_515.65.01_linux.run
```





## 방화벽 설정

- https://avaiable.tistory.com/153


- firewalld 사용