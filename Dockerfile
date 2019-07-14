
FROM	node:10	AS	frontend
RUN	mkdir /static_build
WORKDIR	/static_build
COPY	eahub/base/static	eahub/base/static
COPY	package.json	package-lock.json	webpack.config.js	./
RUN	npm ci
RUN	npm run build

FROM	python:3.7
RUN	mkdir /code \
	&& mkdir /static_build
WORKDIR	/code
COPY	requirements.txt	.
RUN	pip install -r requirements.txt
COPY	.	.
ENV	PYTHONPATH	/code
COPY --from=frontend	/static_build/eahub/base/static	/static_build
RUN	mkdir /static \
	&& DJANGO_SETTINGS_MODULE=eahub.config.build_settings django-admin collectstatic
ENV	DJANGO_SETTINGS_MODULE	eahub.config.settings
EXPOSE	8000
CMD	["gunicorn","--bind=0.0.0.0:8000","eahub.config.wsgi"]
