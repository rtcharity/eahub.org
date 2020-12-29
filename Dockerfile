
FROM	node:10	AS	frontend
COPY	eahub/base/static	eahub/base/static
COPY	package.json	package-lock.json	webpack.config.js tsconfig.json	./
RUN	npm ci
RUN	npm run build

FROM	python:3.7
RUN	mkdir /app \
	&& mkdir /static_build
WORKDIR	/app
COPY	requirements.txt	.
RUN	pip install -r requirements.txt
COPY	.	.
ENV	PYTHONPATH	/app
ARG buildfolder=/static_build
ENV buildfolder=${buildfolder}
COPY --from=frontend	/eahub/base/static $buildfolder
RUN	mkdir /static
RUN DJANGO_SETTINGS_MODULE=eahub.config.build_settings django-admin collectstatic --ignore=node_modules
ENV	DJANGO_SETTINGS_MODULE	eahub.config.settings
EXPOSE	8000
CMD	["gunicorn","--bind=0.0.0.0:8000","eahub.config.wsgi"]
