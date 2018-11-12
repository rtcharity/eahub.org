# Requirements
- Python 3
- [Docker Compose](https://docs.docker.com/compose)

# Running locally
Create a `.env` file with:
```
DATABASE_NAME=<see lastpass>
DATABASE_USERNAME=<see lastpass>
DATABASE_PASSWORD=<see lastpass>
DATABASE_HOST=<see lastpass>
```
Then run:
```
$ docker-compose up
```

# Running django commands
- Run the stack locally `$ docker compose up`
- List running docker containers `$ docker ps`
- Get the docker `CONTAINER ID` from the response and run `docker exec -t -i 66175bfd6ae6 bash`
Useful commands:
```
$ python manage.py makemigrations
$ python manage.py migrate
```