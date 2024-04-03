FROM python:3.8
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "-u", "coronavirusapi_exporter.py"]