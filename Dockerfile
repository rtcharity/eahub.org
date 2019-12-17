
FROM	node:10	AS	frontend
COPY	eahub/base/static	eahub/base/static
COPY	package.json	package-lock.json	webpack.config.js	./
RUN	npm ci
RUN	npm run build
RUN ls eahub/base/static

FROM	python:3.7
RUN	mkdir /code \
	&& mkdir /static_build
WORKDIR	/code
COPY	requirements.txt	.
RUN	pip install -r requirements.txt
COPY	.	.
ENV	PYTHONPATH	/code
ENV PROD True
ARG buildfolder=/static_build
COPY --from=frontend	/eahub/base/static $buildfolder
ARG prod=True
RUN	mkdir /static \
	&& if [ "${prod}" = "True" ]; then DJANGO_SETTINGS_MODULE=eahub.config.build_settings django-admin collectstatic; \
	else DJANGO_SETTINGS_MODULE=eahub.config.build_settings_env django-admin collectstatic; \
	fi;
ENV	DJANGO_SETTINGS_MODULE	eahub.config.settings
EXPOSE	8000
CMD	["gunicorn","--bind=0.0.0.0:8000","eahub.config.wsgi"]
