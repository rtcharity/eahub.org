Backend for [https://eahub.azurewebsites.net](https://eahub.azurewebsites.net)

![eahub.org reboot](https://i.imgur.com/02FNAlY.png)

# Setup
Make sure to have Python3 & [Docker Compose](https://docs.docker.com/compose) installed.

Create a `.env` file with:
```
DEBUG_MODE=True
DATABASE_HOST=<see lastpass>
DATABASE_NAME=<see lastpass>
DATABASE_USERNAME=<see lastpass>
DATABASE_PASSWORD=<see lastpass>
```

# Running
```
$ docker-compose up
```

# Deploying
After uploading a new docker image, the website will automatically update
```
$ docker build -t eahub:latest .
$ y | docker system prune
$ docker tag eahub eahub.azurecr.io/eahub:latest
$ docker push eahub.azurecr.io/eahub:latest
```

# Running django commands
```
$ docker compose up
$ docker ps
$ docker exec -t -i 66175bfd6ae6 bash

$ python manage.py makemigrations
$ python manage.py migrate
```

# Docker Image Registry Login
- Images are privatly saved to our Azure Container Registry
- Remember to create the `.env` file which can be found on lastpass
```
$ docker login eahub.azurecr.io
>>> username: eahub
>>> password: <see lastpass>
```

# Database Login
- We have a fully managed PostgreSQL database hosted by Azure now. This way Microsoft will keep it updated and secure without us having to host a server, it's also significantly cheaper than using a VM instance and easier to scale.
- Feel free to login using a database management app like [TablePlus](https://tableplus.io) for OSX after adding your personal IP address to the whitelist on Azure.
- Login details are on lastpass