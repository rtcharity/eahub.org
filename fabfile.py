from fabric.api import local
from fabric import operations

def build():
    local('docker build -t eahub:latest .')
    local('y | docker system prune')

def run():
    local('docker-compose run --service-ports web') #  with ipdb support
    # local('docker-compose up') #  without ipdb support

def deploy():
    build()
    local('docker tag eahub eahub.azurecr.io/eahub:latest')
    local('docker push eahub.azurecr.io/eahub:latest')

def bash():
    local('docker ps')
    container_id = operations.prompt('Enter container_id from above: ')
    local('docker exec -t -i {container_id} bash'.format(
        container_id=container_id
    ))