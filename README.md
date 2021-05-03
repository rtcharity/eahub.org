Backend for [https://eahub.org](https://eahub.org)

![eahub.org reboot](https://i.imgur.com/02FNAlY.png)

# Setup

- Make sure to have Docker Compose 2 and Nodejs 10.X installed.
- npm ci
- npm run build-watch
- docker-compose run --rm web bash -c "python manage.py migrate" (only necessary when you're setting it up for the first time or pulled python migration changes)
- docker-compose up web

If everything went well, you should be able to get the Hub at http://localhost:8000

If requirements.txt or Dockerfile have changed since last time you built the project, you'll need to run `docker-compose build`.

If `package.json` changes - run `npm install` to generate a new `package-json.lock`.

You can access the email server at localhost:1080.

# Running Tests
```
docker-compose run --rm web pytest
npm test
```

Running a particular python test, e.g., test_localgroups_model.py:  
```
docker-compose run --rm web pytest eahub/tests/test_localgroups_model.py
```

# Debugging python code  

To debug the python code in the docker container:  
1) Add ```import ipdb``` to the python file you want to debug
2) Add ```ipdb.set_trace()``` on the line where you want to set a breakpoint  
3) Run ```docker-compose run --service-ports web``` 



## Formatting Code
```
docker-compose run --rm web black eahub
```
You must run this before sending a pull request or else it will be automatically blocked from merging.

You can also automatically sort your imports:
```
docker-compose run --rm web isort -rc --atomic eahub
```

# Running django commands
```
docker-compose run --rm web bash
docker-compose run --rm web bash -c "python manage.py shell_plus"
docker-compose run --rm web bash -c "python manage.py makemigrations"
docker-compose run --rm web bash -c "python manage.py migrate"
```

# Browser Support Policy

We support the most recent version of Google Chrome, Mozilla Firefox, Safari, and Microsoft Edge.