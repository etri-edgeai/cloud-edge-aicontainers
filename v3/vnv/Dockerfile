FROM python:3.9
WORKDIR /service
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . ./
COPY ./app ./app
ENTRYPOINT ["bash", "app/00_hi.sh"]