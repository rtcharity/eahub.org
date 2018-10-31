# Overview
- Backend for: [https://eahub.azurewebsites.net](https://eahub.azurewebsites.net/)
- Deployment works using [Docker + Azure](https://medium.com/@alexjsanchez/creating-and-deploying-a-flask-app-with-docker-on-azure-in-5-easy-9f7aa7a12145) instructions

# Commands
I've set up [Fabric](http://www.fabfile.org) to make life easier.
```
$ fab run
$ fab deploy
```

# Docker Login
```
$ docker login eahub.azurecr.io
>>> username: eahub
>>> password: lW93AW4SfxOpdCv5b6Rebv/CTvDUXvOq
```