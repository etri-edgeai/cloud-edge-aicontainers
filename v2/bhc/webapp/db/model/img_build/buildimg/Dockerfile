FROM python:3.8

ARG model_file
WORKDIR .
ADD ./$model_file ./home/

RUN apt-get update && apt-get install -y sudo
RUN chmod +w /etc/sudoers
RUN echo 'irteam ALL=(ALL) NOPASSWD:ALL' | tee -a /etc/sudoers
RUN chmod -w /etc/sudoers
RUN sudo apt-get install -y libgl1-mesa-glx
RUN sudo apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install -r home/requirements.txt

ENTRYPOINT ["bash"]