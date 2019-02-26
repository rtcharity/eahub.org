	
FROM	python:3.6
RUN	mkdir /code/
COPY	.	/code/eahub_e2e/
WORKDIR	/code/
RUN	pip install -r eahub_e2e/requirements.txt
ENV	PYTHONPATH	/code/	PYTHONDONTWRITEBYTECODE	True
CMD	["pytest","--driver=Remote"]
