# Setup  

Instructions for developers on how to build and run the project, how to run tests and debug.    

## Requirements  
- [Docker Compose](https://docs.docker.com/compose/install/)  and [Docker Enginge](https://docs.docker.com/engine/install/)
  - You might find it easiest to simply install [Docker Desktop](https://www.docker.com/products/docker-desktop), which 
    comes with Docker Compose and Engine.  
- [Nodejs 10.x](https://nodejs.org/en/download/) (or higher)     

## Run project locally

### Running first time  
- Clone [repo](https://github.com/rtcharity/eahub.org)  
- Build and run frontend  
  - In main folder, run ```npm ci``` to install node dependencies  
  - Run ```npm run build-watch``` to serve frontend files    
- Build and run backend
  - In main folder in separate terminal window, run ```docker-compose run --rm web bash -c "python manage.py migrate"``` 
    to build docker container and create database tables  
  - Run ```docker-compose up web``` to start docker container  
- Project will be served on ```localhost:8000```  
- The email client will be served on ```localhost:1080```  

### Running after changes to ```packages.json```  
```npm install```  
You have to run this if new node dependencies have been added since you've last built the project.  

### Running after changes to ```requirements.txt```  
```docker-compose build --no-cache web```  
You have to run this if new python dependencies have been added since you've last built the project in order to rebuild 
the django backend.    

### Running after adding new python package 
```docker-compose run --rm web bash -c "pip-compile requirements.in > requirements.txt"```   
You have to run this if you want to a new python package.    

### Running after new migration files have been added     
```docker-compose run --rm web bash -c "python manage.py migrate"```  
You have to run this if new migration files have been added since you've last built the project.  

### Create migration files after making changes to django models  
```docker-compose run --rm web bash -c "python manage.py makemigrations"```  
If you've made changes to any of the django models, you will have to run this command to create database migration files.  


## Running tests  
```
docker-compose run --rm web pytest  
```
This will run all tests, including end-to-end.  

Running a particular python test, e.g., test_localgroups_model.py:  
```
docker-compose run --rm web pytest eahub/localgroups/tests/test_localgroups_model.py
```  

## Formatting  
Run automatic formatting:  
```
docker-compose run --rm web black eahub
```
You must run this before sending a pull request or else it will be automatically blocked from merging.

You can also automatically sort your imports:
```
docker-compose run --rm web isort -rc --atomic eahub
```


## Admin panel  
- To access the admin panel locally, you will have to create a superuser: ```docker-compose run --rm web bash -c "python manage.py createsuperuser"```  
- Then log in with the chosen username and password and go to localhost:8000/admin  

## Debugging python code  

To debug the python code in the docker container:  
1) Add ```import ipdb``` to the python file you want to debug
2) Add ```ipdb.set_trace()``` on the line where you want to set a breakpoint  
3) Run ```docker-compose run --service-ports web```  

## Troubleshooting  

A list of common issues  

### Docker Engine not running    
* Error message:
```
docker.errors.DockerException: Error while fetching server API version: (2, 'CreateFile', 'The system cannot find the file specified.')
[2888] Failed to execute script docker-compose
```
* Fix: Make sure Docker Engine is running  

### Filesharing not enabled  
* Error message:  
```
ERROR: for db  Cannot create container for service db: status code not OK but 500: \u02d9\u02d9\u02d9\u02d9
FDocker.Core, Version=3.4.0.64130, Culture=neutral, PublicKeyToken=null
Docker.Core.DockerException ClassNameMessageDataInnerExceptionHelpURLStackTraceStringRemoteStackTraceStringRemoteStackIndexExceptionMethodHRWatsonBucketsSystem.Collections.IDictionarySystem.Exception
Docker.Core.DockerExceptionFilesharing has been cancelled    
```  
* Fix: Enable file sharing in docker for the local directory into which you have cloned the repo  

### Node dependencies not installed  
* Error message:  
```
> eahub.org@0.0.0 build-watch C:\Users\sebja\code\eahub.org-test
> webpack-dev-server --config webpack.config.js

'webpack-dev-server' is not recognized as an internal or external command,
operable program or batch file.

```   
* Fix: Run ```npm ci```  
