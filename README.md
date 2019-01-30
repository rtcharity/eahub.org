Backend for [https://eahub.azurewebsites.net](https://eahub.azurewebsites.net)

![eahub.org reboot](https://i.imgur.com/02FNAlY.png)

# Setup

1.  Make sure to have [Docker Compose](https://docs.docker.com/compose)
    installed.

1.  Add the following line to your hosts file (`/etc/hosts` on Mac or Linux,
    `%SystemRoot%\System32\drivers\etc\hosts` on Windows):
    ```
    127.0.0.1 objstore
    ```

1.  ```
    docker-compose run web django-admin createcontainer
    ```

1.  ```
    docker-compose run web django-admin migrate
    ```

# Running
```
$ docker-compose up
```

If the Dockerfile has changed since last time you did this, you'll need to run
`docker-compose up --build` or `docker-compose build`.

If the database schema has changed since last time, you'll need to run
`docker-compose run web django-admin migrate`.

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
$ docker-compose run web bash
$ docker-compose run web django-admin shell
$ docker-compose run web django-admin makemigrations
$ docker-compose run web django-admin migrate
```

# Docker Image Registry Login
- Images are privately saved to our Azure Container Registry
```
$ docker login eahub.azurecr.io
>>> username: eahub
>>> password: <see lastpass>
```
