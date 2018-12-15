FROM python:3.6

RUN mkdir -p /code
WORKDIR /code

RUN pip install django==2.1.4 gunicorn==19.9.0 psycopg2-binary==2.7.6.1 pytz==2018.7 whitenoise==4.1.2 requests==2.21.0

COPY . /code/

EXPOSE 8000

COPY init.sh /usr/local/bin/
	
RUN chmod u+x /usr/local/bin/init.sh
ENTRYPOINT ["init.sh"]