import os 
from fabric.api import local

def _build():
    local('docker build -t eahub:latest .')
    local('y | docker system prune')

def run():
    _build()
    local('docker-compose build')
    print('\033[94m ----------> Site running @ http://0.0.0.0:5000 <---------- \033[0m')
    local('docker-compose run --service-ports web')

def deploy():
    _build()
    local('docker tag eahub eahub.azurecr.io/eahub:latest')
    local('docker push eahub.azurecr.io/eahub:latest')
    print('Image will slowly be updated to: http://40.91.201.107')

# notes
# http://containertutorials.com/docker-compose/flask-simple-app.html
# https://cloud.google.com/container-registry/docs/quickstart