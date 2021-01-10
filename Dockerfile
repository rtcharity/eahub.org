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
COPY eahub/base/static/ .
RUN npm ci
RUN npm run build


COPY . .
RUN python manage.py collectstatic --ignore=node_modules


EXPOSE 8000
CMD ["gunicorn","--bind=0.0.0.0:8000","eahub.config.wsgi"]
