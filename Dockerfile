FROM python:3.6

RUN mkdir -p /opt/services/djangoapp/src
WORKDIR /opt/services/djangoapp/src

RUN pip install gunicorn django psycopg2-binary whitenoise

COPY . /opt/services/djangoapp/src

EXPOSE 8000

COPY init.sh /usr/local/bin/
	
RUN chmod u+x /usr/local/bin/init.sh
ENTRYPOINT ["init.sh"]