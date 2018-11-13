from fabric.api import local

def run():
    local('docker-compose up')

def deploy():
    local('docker build -t eahub:latest .')
    local('y | docker system prune')
    local('docker tag eahub eahub.azurecr.io/eahub:latest')
    local('docker push eahub.azurecr.io/eahub:latest')