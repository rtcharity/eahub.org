Backend for [https://eahub.org](https://eahub.org)

![eahub.org reboot](https://i.imgur.com/02FNAlY.png)

# Setup

1.  Make sure to have [Docker Compose](https://docs.docker.com/compose)
    installed.

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

If the Dockerfile has changed since last time you did this, you'll need to run
`docker-compose up --build` or `docker-compose build`.

If the database schema has changed since last time, you'll need to run
`docker-compose run web django-admin migrate`.

# Running End-to-End Tests
```
$ docker-compose run e2e
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
- Every commit in a pull request needs a `Signed-off-by:` line, which you can
  generate with the `-s` option of `git commit`. By including this line, you
  attest to the
  [Developer Certificate of Origin](https://developercertificate.org/), i.e.,
  you agree to release your contribution under the [MIT License](LICENSE) and
  certify that you have the right to do so. Pull requests that don't have this
  in every commit will be automatically blocked from merging. Maintainers should
  ensure that this line is preserved in the squashed commit (but only once per
  contributor per commit).
