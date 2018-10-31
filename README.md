# Overview
Backend for: [https://eahub.azurewebsites.net](https://eahub.azurewebsites.net/)

# Running Locally
Setup:
```
$ pip3 install -r requirements.txt
$ export FLASK_APP=application.py
```

Running:
```
$ export FLASK_APP=application.py
$ python3 -m flask run
```

# Deploying
Taken from Taken from the [azure docs](https://docs.microsoft.com/en-us/azure/app-service/containers/quickstart-python)

Setup:
```
$ az login
$ az webapp deployment user set --user-name cli_eahub --password cli_password_1
$ git remote add azure http://eahub@eahub.scm.azurewebsites.net/eahub.git
```

Deploying:
```
git push azure master
```

# Config
- See [utils/Settings.py](utils/Settings.py) for app settings

MYSQL Server:
```
{
    "host": "eahub.mysql.database.azure.com"
    "port": 3306
    "username": "eahub@eahub"
    "password: "password_5rlvsk959wV4iTR908ScAPPiThGY7URBOZv0hx2Ref2NJvjE9OAH4ky77dHI"
    "database": "eahub"
}
```