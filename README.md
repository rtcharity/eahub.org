Backend for [https://eahub.org](https://eahub.org)

![eahub.org reboot](https://i.imgur.com/02FNAlY.png)

[![Build Status](https://dev.azure.com/rtcharity/eahub.org/_apis/build/status/rtcharity.eahub.org?branchName=master)](https://dev.azure.com/rtcharity/eahub.org/_build/latest?definitionId=1&branchName=master)

# Setup

1.  Make sure to have [Docker Compose](https://docs.docker.com/compose)
    installed. (Note: You may need to follow these [post-installation steps](https://docs.docker.com/install/linux/linux-postinstall/).)

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

If everything went well, you should have a number of containers now being served (use `docker ps` to get a list of them).
You should be able to get the Hub at http://localhost:8000.

If the Dockerfile has changed since last time you did this, you'll need to run
`docker-compose up --build` or `docker-compose build`.

If the database schema has changed since last time, you'll need to run
`docker-compose run web django-admin migrate`.

# Rebuilding frontend in development

To see live changes to the frontend while developing, open a new terminal window and run the following command from the main folder:
`npm run build-watch`

To see the changes, make a hard refresh in your browser.

# Running Tests
```
$ docker-compose run --use-aliases web pytest
```

## Running Frontend Tests
Run ```npm test```  

# Formatting Code
```
$ docker-compose run web black .
```
You must run this before sending a pull request or else it will be automatically blocked from merging.

You can also automatically sort your imports:

```
$ docker-compose run web isort -rc --atomic .
```

# Deploying
After uploading a new docker image, the website will automatically update
```
$ cd eahub
$ docker build -t eahub:latest .
$ docker system prune --force
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
