FROM python:3.8.15

WORKDIR .
ADD ./model.tar.gz ./home/

RUN apt-get update && apt-get install -y sudo
RUN chmod +w /etc/sudoers
RUN echo 'irteam ALL=(ALL) NOPASSWD:ALL' | tee -a /etc/sudoers
RUN chmod -w /etc/sudoers
RUN sudo apt-get install -y libgl1-mesa-glx
RUN sudo apt-get install -y python3-pip
RUN pip install --upgrade pip
RUN pip3 install torch torchvision torchaudio
RUN pip install ultralytics