![eahub.org reboot](https://i.imgur.com/02FNAlY.png)

- Backend for: [http://51.145.154.197](http://51.145.154.197/)
- Deployment works using [Docker + Azure](https://medium.com/@alexjsanchez/creating-and-deploying-a-flask-app-with-docker-on-azure-in-5-easy-9f7aa7a12145) instructions

# Requirements
* python 2.7
* mysql-server libmysqlclient-dev (seems to be required by mysql connector)
* Fabric 2.0 (optional pip install)
* Create a `secrets.env` file in the root directory which looks like [this](https://gist.github.com/Manoj-nathwani/3c956a0aa17aec2959fc95f53d1e8af6)

# Commands
With [Fabric](http://www.fabfile.org) installed:
```
$ fab run
$ fab deploy
```

Going vanilla without fabric:
```
# run
$ docker-compose build
$ docker-compose run --service-ports web

# deploy
$ docker tag eahub eahub.azurecr.io/eahub:latest
$ docker push eahub.azurecr.io/eahub:latest
```

# Docker Image Registry Login
- Images are privatly saved to our [Container Registry](https://portal.azure.com/#@dotimpact.org/resource/subscriptions/72a43e63-c361-434d-9b55-34301c8aa920/resourceGroups/eahub/providers/Microsoft.ContainerRegistry/registries/eahub/overview) on Azure
```
$ docker login eahub.azurecr.io
>>> username: eahub
>>> password: <see lastpass>
```

# Database
- We have a fully managed MySQL database hosted by Azure now. This way Microsoft will keep it updated and secure without us having to host a server, it's also significantly cheaper than using a VM instance and easier to scale.
- Feel free to login using a database management app like [Sequel Pro](https://www.sequelpro.com) for OSX after adding your personal IP address to the whitelist on Azure.
```
{
    "host": "eahub.mysql.database.azure.com",
    "port": 3306,
    "username": "eahub@eahub",
    "password": <see lastpass>
}
```
