# django-gdrive-crud-app

[Django-based Google Drive CRUD app](https://github.com/opheron/django-gdrive-crud-app)

## Features

1. Authenticate the user using OAuth 2.0.
2. List files in the user’s Google Drive.
3. Upload a file to the user’s Google Drive.
4. Download a file from the user’s Google Drive.
5. Delete a file from the user’s Google Drive.


## Design & Architecture
Skeleton code came from [![Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
Formatting and linting is done with [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

### Installation via Docker

This project was primarily intended to be run with Docker, but can be installed locally.

To create local Docker build, go to the repo root folder in terminal and do:

```shell
docker compose -f docker-compose.local.yml build
```

Run the docker local dev build by running:

```shell
docker compose -f docker-compose.local.yml up
```

To run in a detached (background) mode, do:

$ docker compose up -d

In order to run docs service you can run:

$ docker compose -f docker-compose.docs.yml up

To run the docs with local services just use:

$ docker compose -f docker-compose.local.yml -f docker-compose.docs.yml up

The site should start and be accessible at: http://localhost:3000

After getting everything running on docker, do:

```shell
docker compose -f docker-compose.local.yml run --rm django python manage.py migrate
docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser
docker compose -f docker-compose.local.yml run --rm django python manage.py startapp gdrivecrud
```

### Google Cloud API setup

Create a Google Cloud app called "django-gdrive-crud-app". (see: https://developers.google.com/drive/api/quickstart/js)

Go to Google API OAuth 2.0 Client ID: https://console.cloud.google.com/
"Create credentials" -> "OAuth Client ID"
"Application Type": Web application
"Name": django-gdrive-crud-app-client
"Authorized JavaScript origins": (none - leave blank)
"Authorized redirect URIs": http://localhost:3000/accounts/google/login/callback/

Note: During OAuth, strict browser security settings may cause the OAuth flow to error. If so, try setting the authorizing browser to Chrome and removing strict browser security settings.

Add a SocialApp (socialaccount app) containing the required client credentials, or, make sure that these are configured via the SOCIALACCOUNT_PROVIDERS[<provider>]['APP'] setting (see example above).

In order for the app to work, you must have an OAuth Social Account for Google API set up.

## Settings
See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

See cookiecutter-django [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy django_gdrive_crud_app

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest
