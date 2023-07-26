FROM python:3.8.15

MAINTAINER keti <ethicsense@keti.re.kr>

WORKDIR /home/

## download scripts
ADD get-docker.sh .
ADD grafana-enterprise_10.0.1_amd64.deb .

## EVC modules
ADD evc.tar.gz .

## set env
RUN apt-get update && apt-get install -y sudo
RUN chmod +w /etc/sudoers
RUN echo 'irteam ALL=(ALL) NOPASSWD:ALL' | tee -a /etc/sudoers
RUN chmod -w /etc/sudoers
RUN sudo apt-get install -y libgl1-mesa-glx
RUN sudo apt-get install -y python3-pip
RUN pip install --upgrade pip
RUN pip install ansible
RUN sh get-docker.sh
RUN sudo apt-get install -y adduser libfontconfig1
RUN sudo dpkg -i grafana-enterprise_10.0.1_amd64.deb