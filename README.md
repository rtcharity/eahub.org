Backend for [https://eahub.org](https://eahub.org)

![eahub.org reboot](https://i.imgur.com/02FNAlY.png)

[![Build Status](https://dev.azure.com/rtcharity/eahub.org/_apis/build/status/rtcharity.eahub.org?branchName=master)](https://dev.azure.com/rtcharity/eahub.org/_build/latest?definitionId=1&branchName=master)

# Setup

- Make sure to have Docker Compose 3 and Nodejs 10.X installed.
- npm ci
- npm run build-watch
- docker-compose run --rm web django-admin migrate
- docker-compose up

If everything went well, you should be able to get the Hub at http://localhost:8000

If the Dockerfile has changed since last time you did this, you'll need to run
`docker-compose up --build` or `docker-compose build`.

If `package.json` changes - run `npm install` to generate a new `package-json.lock`.

If the database schema has changed since last time, you'll need to run
`docker-compose run --rm web django-admin migrate`.

### Pulling the db & media to your local instance
- receive access to https://control.divio.com/control/71735/edit/88402/
- add an ssh key to your profile https://control.divio.com/account/ssh-keys/
- cp .divio/config-example.json .divio/config.json
- pip install divio-cli
- divio login
- divio project pull db test
- divio project pull media test

You can also push the db & media, but don't do it without getting the approval from Sebastian or Victor.

You can drop the local and test server db though running:
- docker-compose stop db
- docker-compose rm db
- docker-compose run --rm web django-admin migrate
- divio project push db test

### Links
- stage server - https://eahub-stage.us.aldryn.io/
- deployment control panel - https://control.divio.com/control/71735/edit/88402/

# Running Tests
```
docker-compose run --rm web pytest
npm test
```

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
docker-compose run --rm web django-admin shell
docker-compose run --rm web django-admin makemigrations
docker-compose run --rm web django-admin migrate
```

# Browser Support Policy

We support the most recent version of Google Chrome, Mozilla Firefox, Safari, and Microsoft Edge.

We support browsers with JavaScript disabled, but they will receive a degraded experience without dynamic client-side functionality. Because our JavaScript works only in modern browsers, legacy browsers like Internet Explorer receive the same degraded experience.

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
