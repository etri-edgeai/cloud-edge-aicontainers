-----------------------------------------------------
# 기술문서 
 - 기술문서명 : 연합학습을 위한 GPU(CUDA)환경 설정
 - 과제명 : 능동적 즉시 대응 및 빠른 학습이 가능한 적응형 경량 엣지 연동분석 기술개발
 - 영문과제명 : Development of Adaptive and Lightweight Edge-Collaborative Analysis Technology for Enabling Proactively Immediate Response and Rapid Learning
 - Acknowledgement : This work was supported by Institute of Information & communications Technology Planning & Evaluation (IITP) grant funded by the Korea government(MSIT) (No. 2021-0-00907, Development of Adaptive and Lightweight Edge-Collaborative Analysis Technology for Enabling Proactively Immediate Response and Rapid Learning).
 - 작성자 : 박종빈
-----------------------------------------------------


- 참고 주소 : https://pyimagesearch.com/2019/12/09/how-to-install-tensorflow-2-0-on-ubuntu/
- 위 주소의 경우 2019년 12월 자료로써, cuda 버전은 최신 자료를 바탕으로 수정이 필요합니다.

## Step 01: Install Ubuntu + TensorFlow 2.0 deep learning dependencies

```bash
    $ sudo apt-get update
    $ sudo apt-get upgrade
    $ sudo apt-get install build-essential cmake unzip pkg-config
    $ sudo apt-get install gcc-6 g++-6
    $ sudo apt-get install screen
    $ sudo apt-get install libxmu-dev libxi-dev libglu1-mesa libglu1-mesa-dev
    $ sudo apt-get install libjpeg-dev libpng-dev libtiff-dev
    $ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
    $ sudo apt-get install libxvidcore-dev libx264-dev
    $ sudo apt-get install libopenblas-dev libatlas-base-dev liblapack-dev gfortran
    $ sudo apt-get install libhdf5-serial-dev
    $ sudo apt-get install python3-dev python3-tk python-imaging-tk
    $ sudo apt-get install libgtk-3-dev
```


## Step 02 (GPU-only): Install NVIDIA drivers, CUDA, and cuDNN

```bash
    $ sudo add-apt-repository ppa:graphics-drivers/ppa
    $ sudo apt-get update
    $ sudo apt-get install nvidia-driver-xxx # 여기는 시스템 환경에 따라 달라질 수 있음
    $ sudo reboot now
    $ nvidia-smi
```

- NVIDIA, pytorch, tensorflow 홈페이지에 방문하여 버전 확인후 설치가 필요합니다.

- pytorch
```bash
    https://pytorch.org/
```

- NVIDIA
```bash
    https://developer.nvidia.com/cuda-11-6-2-download-archive?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=20.04&target_type=deb_local
```

- tensorflow
```bash
    https://www.tensorflow.org/?hl=ko
```

### CUDA 11.6

```bash
$ pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
$ sudo apt install nvidia-cuda-toolkit
```

### CUDA 11.7

```bash
$ pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117
$ sudo apt install nvidia-cuda-toolkit
```


## PyTorch 예제

```bash

import torch
 
#  Returns a bool indicating if CUDA is currently available.
torch.cuda.is_available()
#  True
 
#  Returns the index of a currently selected device.
torch.cuda.current_device()
#  0
 
#  Returns the number of GPUs available.
torch.cuda.device_count()
#  1
 
#  Gets the name of a device.
torch.cuda.get_device_name(0)

 
#  Context-manager that changes the selected device.
#  device (torch.device or int) – device index to select. 
torch.cuda.device(0)

```


- example

```bash

import torch
 
# Default CUDA device
cuda = torch.device('cuda')
 
# allocates a tensor on default GPU
a = torch.tensor([1., 2.], device=cuda)
 
# transfers a tensor from 'C'PU to 'G'PU
b = torch.tensor([1., 2.]).cuda()
 
# Same with .cuda()
b2 = torch.tensor([1., 2.]).to(device=cuda)


```



## Jupyterlab 설치

```bash
    $ pip3 install jupyterlab
```
