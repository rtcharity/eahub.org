# Overview
[https://eahub.azurewebsites.net](https://eahub.azurewebsites.net/)

# Deploying
Taken from Taken from the [azure docs](https://docs.microsoft.com/en-us/azure/app-service/containers/quickstart-python)

## Setup
```
$ az login

$ az webapp deployment user set --user-name cli_eahub --password cli_password_1

$ git remote add azure http://eahub@eahub.scm.azurewebsites.net/eahub.git
```

## Deploying
```
git push azure master
```