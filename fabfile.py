from fabric.api import local

def build():
    local('docker build -t eahub:latest .')
    local('y | docker system prune')

def run():
    local('docker-compose up')

def deploy():
    build()
    local('docker tag eahub eahub.azurecr.io/eahub:latest')
    local('docker push eahub.azurecr.io/eahub:latest')