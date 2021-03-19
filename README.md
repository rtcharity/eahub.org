Backend for [https://eahub.org](https://eahub.org)

![eahub.org reboot](https://i.imgur.com/02FNAlY.png)

# Setup

- Make sure to have Docker Compose 3 and Nodejs 10.X installed.
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

# Commit Message Practices

These are primarily for the benefit of maintainers, but all contributors are
urged to follow them in order to make maintainers' lives easier.

- In general, follow the practices outlined in
  ["How to Write a Git Commit Message"](https://chris.beams.io/posts/git-commit/)
  by Chris Beams.
- As an exception to the above, do not manually wrap the body of a commit
  message. The main reason for this is because our workflow depends on the
  GitHub web interface, which doesn't provide an easy way to do this. It does
  not depend on emailing patches, so the benefits of wrapped lines don't apply.
  There is arguably some benefit to the usability of `git log`, but it doesn't
  outweigh the costs.
- Maintainers should use GitHub's
  [squash merging](https://help.github.com/en/articles/about-pull-request-merges#squash-and-merge-your-pull-request-commits)
  exclusively. Merge commits and rebase merging have been disabled in GitHub.
