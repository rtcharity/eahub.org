from fabric import operations
from fabric.api import local


def build():
    local("docker-compose build")
    local("docker build -t eahub:latest .")
    local("y | docker system prune")


def run():
    local("docker-compose run --service-ports web")  # with ipdb support
    # local('docker-compose up') #  without ipdb support


def makemigrations():
    local("docker-compose run web django-admin makemigrations")


def migrate():
    local("docker-compose run web django-admin migrate")


def bash():
    local("docker ps")
    container_id = operations.prompt("Enter container_id from above: ")
    local("docker exec -t -i {container_id} bash".format(container_id=container_id))
