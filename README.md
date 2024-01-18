# vigilant-waffle

## Build & Run

Create `ops/.env` file with following content, replace values with your own:
```shell
POSTGRES_DB=app
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

API__SECRET_KEY="<generate an unique string here>"
```

Run docker-compose services:
```shell
sh run.sh
```

Create your admin user:
```shell
docker-compose -f ops/docker-compose.yaml exec api poetry run python manage.py createsuperuser
```

Open http://localhost:8000/api/ and login with your credentials.

## Stop & Cleanup
```shell
sh stop.sh
rm -rf data/postgres-data
```


## Development

### [Pre-commit](https://pre-commit.com/)

To use industry level standards we are using back, flake8, mypy

Please install "pre-commit" and all dependencies before do any commit.

```shell
pip install pre-commit
pre-commit
pre-commit install
```

## Packages used

[Django REST Framework](https://www.django-rest-framework.org/) - to boostrap & simplify REST api building routine

**pytest** - library for testing
**pytest-django** - pytest plugin for django, with useful fixtures to simplify testing django apps
**faker** - lib to generate random data for testing fixtures


## Project structure

```
├── LICENSE
├── README.md
├── api
│   ├── Dockerfile
│   ├── api
│   ├── applications
│   ├── docker-entrypoint.sh
│   ├── manage.py
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── pytest.ini
│   └── users
├── data
│   └── postgres-data
├── ops
│   └── docker-compose.yaml
├── run.sh
└── stop.sh
```

 * `api` - Django project root folder
 * `api/Dockerfile` - Dockerfile for Django app
 * `api/api` - Django project settings folder
 * `api/applications`, `api/users` - Django apps folders
 * `ops/` - docker-compose files and other ops files like `.env`
 * `data/` - folder for persistent data like database
 * `run.sh`, `stop.sh` - scripts to run/stop docker-compose services
