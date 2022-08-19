# 연합학습을 위한 GPU(CUDA)환경 설정

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
