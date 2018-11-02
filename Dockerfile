# Use an official Python runtime as a parent image
FROM python:2.7-slim-jessie

WORKDIR /app
ADD . /app

RUN apt-get update
RUN apt-get install -y gcc
RUN apt install -y libmysqlclient-dev
RUN pip install --trusted-host pypi.python.org -r config/requirements.txt

CMD ["python", "app.py"]