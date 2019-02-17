	
FROM	python:3.6
COPY	.	/code/
WORKDIR	/code/
RUN	pip install -r requirements.txt
ENV	PYTHONPATH	/code/
RUN	mkdir /static/ \
	&& DJANGO_SETTINGS_MODULE=eahub.config.build_settings django-admin collectstatic
ENV	DJANGO_SETTINGS_MODULE	eahub.config.settings
EXPOSE	8000
CMD	["gunicorn","--bind=0.0.0.0:8000","eahub.config.wsgi"]
