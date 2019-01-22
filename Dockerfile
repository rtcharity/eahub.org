FROM python:3.6
COPY . /code/
WORKDIR /code/
RUN pip install -r requirements.txt
ENV PYTHONPATH=/code/ DJANGO_SETTINGS_MODULE=eahub.settings
EXPOSE 8000
CMD ["gunicorn", "--bind=0.0.0.0:8000", "eahub.wsgi"]
