FROM python:3.8

WORKDIR .
ADD ./model.tar.gz ./home/


RUN pip3 install --upgrade pip
RUN pip3 install -r home/requirements.txt

ENTRYPOINT ["bash"]
