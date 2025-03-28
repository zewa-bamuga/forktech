# Terms of reference for the Forktech company

## Run locally

### Run with Docker Compose

> :warning: **Linux Users**: Running docker-compose may require using sudo command if current user is not in the docker group

> :warning: **Windows Users**: Check that your `git config core.autocrlf` is `false` or set it to `false` before starting, otherwise build/run may fail

```shell script
	make run
```

or

```shell script
	cp .env.example .env
	cp ./deploy/compose/local/docker-compose.yml docker-compose.yml
	docker-compose up -d
```

### Running tests
```shell script
	make test
```

### Useful Tips

- use http://localhost:80/api/docs to access web Swagger
- use `make logs` to see logs