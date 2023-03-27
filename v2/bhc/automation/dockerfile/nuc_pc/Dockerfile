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
RUN pip install -r home/requirements.txt
RUN pip install torch==1.13.1+cu116 torchaudio==0.13.1+cu116 torchvision==0.14.1+cu116 -f https://download.pytorch.org/whl/cu116/torch_stable.html

ENTRYPOINT ["bash"]