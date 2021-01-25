FROM nikolaik/python-nodejs:python3.7-nodejs10


RUN mkdir /app
RUN mkdir /app/static_build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-deps --no-cache-dir -r requirements.txt


COPY package.json .
COPY package-lock.json .
COPY webpack.config.js .
COPY tsconfig.json .
RUN npm ci
COPY /eahub/base/static/ ./eahub/base/static/
RUN npm run build


COPY . .
RUN python manage.py collectstatic --ignore=node_modules --no-input

EXPOSE 8000
CMD ["gunicorn","--bind=0.0.0.0:8000","eahub.config.wsgi"]
