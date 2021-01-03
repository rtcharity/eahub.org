FROM nikolaik/python-nodejs:python3.7-nodejs10


RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-deps --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH /app


RUN mkdir /static_build
RUN npm ci
RUN npm run build
ARG buildfolder=/static_build
ENV buildfolder=${buildfolder}
COPY /eahub/base/static $buildfolder
RUN mkdir /static
RUN DJANGO_SETTINGS_MODULE=eahub.config.build_settings django-admin collectstatic --ignore=node_modules
ENV DJANGO_SETTINGS_MODULE eahub.config.settings

EXPOSE 8000
CMD ["gunicorn","--bind=0.0.0.0:8000","eahub.config.wsgi"]
