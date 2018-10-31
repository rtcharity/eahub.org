# Overview
- Backend for: [http://40.91.201.107](http://40.91.201.107/)
- Deployment works using [Docker + Azure](https://medium.com/@alexjsanchez/creating-and-deploying-a-flask-app-with-docker-on-azure-in-5-easy-9f7aa7a12145) instructions

# Commands
- I've set up [Fabric](http://www.fabfile.org) to make life super mega easy.
- See the [/fabfile.py](/fabfile.py) for more details.
```
$ fab run
$ fab deploy
```

# Docker Login
- Images are privatly saved to our [Container Registry](https://portal.azure.com/#@dotimpact.org/resource/subscriptions/72a43e63-c361-434d-9b55-34301c8aa920/resourceGroups/eahub/providers/Microsoft.ContainerRegistry/registries/eahub/overview) on Azure
```
$ docker login eahub.azurecr.io
>>> username: eahub
>>> password: lW93AW4SfxOpdCv5b6Rebv/CTvDUXvOq
```

# Database
- We have a fully managed MySQL database hosted by Azure now. This way Microsoft will keep it updated and secure without us having to host a server, it's also significantly cheaper than using a VM instance and easier to scale.
- Feel free to login using a database management app like [Sequel Pro](https://www.sequelpro.com) for OSX after adding your personal IP address to the whitelist on Azure.
```
{
    "host": "eahub.mysql.database.azure.com",
    "port": 3306,
    "username": "eahub@eahub",
    "password": "password_5rlvsk959wV4iTR908ScAPPiThGY7URBOZv0hx2Ref2NJvjE9OAH4ky77dHI"
}
```