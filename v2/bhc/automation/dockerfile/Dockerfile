FROM python:3.8

WORKDIR .
ADD ./model.tar.gz ./home/


RUN pip install --upgrade pip
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install -r home/requirements.txt

ENTRYPOINT ["bash"]
