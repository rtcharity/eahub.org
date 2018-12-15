FROM python:3.6

RUN mkdir -p /code
WORKDIR /code
COPY . /code/

RUN pip install -r requirements.txt

EXPOSE 8000

COPY init.sh /usr/local/bin/
	
RUN chmod u+x /usr/local/bin/init.sh
ENTRYPOINT ["init.sh"]