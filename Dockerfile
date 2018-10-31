# Use an official Python runtime as a parent image
FROM python:2.7-slim-jessie

WORKDIR /app
ADD . /app

RUN apt-get update
RUN apt-get install -y gcc
RUN apt install -y libmysqlclient-dev
RUN pip install --trusted-host pypi.python.org -r config/requirements.txt

ENV DATABASE_CONNECTION_URL mysql+mysqldb://eahub@eahub:password_5rlvsk959wV4iTR908ScAPPiThGY7URBOZv0hx2Ref2NJvjE9OAH4ky77dHI@eahub.mysql.database.azure.com/eahub?charset=utf8

CMD ["python", "app.py"]