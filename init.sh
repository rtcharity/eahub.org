#!/bin/bash
source .env
-e
gunicorn -b 0.0.0.0:8000 eahub.wsgi:application