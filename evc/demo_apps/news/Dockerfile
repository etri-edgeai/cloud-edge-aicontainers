FROM python

WORKDIR /home
ADD ./model.tar.gz .

RUN mkdir -p video
RUN mkdir -p video/out

RUN apt-get update && apt-get install -y sudo
RUN chmod +w /etc/sudoers
RUN echo 'irteam ALL=(ALL) NOPASSWD:ALL' | tee -a /etc/sudoers
RUN chmod -w /etc/sudoers
RUN sudo apt-get install -y libgl1-mesa-glx
RUN sudo apt-get install -y python3-pip
RUN sudo apt-get install -y ffmpeg

# Install Packages
RUN pip install ffmpeg-python
RUN pip install --upgrade pip
RUN pip3 install torch torchvision torchaudio
RUN pip install ultralytics
RUN pip install gradio