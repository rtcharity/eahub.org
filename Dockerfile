FROM nikolaik/python-nodejs:python3.9-nodejs14


RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-deps --no-cache-dir -r requirements.txt


COPY package.json .
COPY package-lock.json .
COPY webpack.config.js .
COPY tsconfig.json .
RUN npm ci
COPY /eahub/base/static/ ./eahub/base/static/
ARG SENTRY_AUTH_TOKEN
ENV SENTRY_AUTH_TOKEN ${SENTRY_AUTH_TOKEN}
RUN SENTRY_AUTH_TOKEN=$SENTRY_AUTH_TOKEN npm run build


COPY . .
RUN mkdir /app/static_build
ENV DJANGO_ENV="docker_build"
RUN python manage.py collectstatic --ignore=node_modules --no-input

EXPOSE 8000
CMD ["gunicorn", "--bind=0.0.0.0:8000", "eahub.config.wsgi"]
