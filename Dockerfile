FROM python:3.6

RUN mkdir -p /code
WORKDIR /code

RUN pip install gunicorn django psycopg2-binary whitenoise

COPY . /code/

EXPOSE 8000

COPY init.sh /usr/local/bin/
	
RUN chmod u+x /usr/local/bin/init.sh
ENTRYPOINT ["init.sh"]