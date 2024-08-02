# django-gdrive-crud-app

[Django-based Google Drive CRUD app](https://github.com/opheron/django-gdrive-crud-app)

## TODO

1. Authenticate the user using OAuth 2.0.
2. List files in the user’s Google Drive.
3. Upload a file to the user’s Google Drive.
4. Download a file from the user’s Google Drive.
5. Delete a file from the user’s Google Drive.

### Specific deliverables:

Write unit tests for individual components.
Write integration tests for end-to-end functionality.
Include instructions on how to run the tests.

### Readme & documentation
Provide a README file with:
◦ An overview of the application.
◦ Instructions on setting up the development environment.
◦ Steps to run the application.
◦ Any assumptions or design decisions made.
• Comment your code where necessary to explain complex logic.

### Video
Create short video (5-10 minutes) demonstrating the application and explaining your
approach


[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

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

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.

### Requirements

Create a Google Cloud app called "django-gdrive-crud-app". (see: https://developers.google.com/drive/api/quickstart/js)

Go to Google API OAuth 2.0 Client ID: https://console.cloud.google.com/
"Create credentials" -> "OAuth Client ID"
"Application Type": Web application
"Name": django-gdrive-crud-app-client
"Authorized JavaScript origins": (none - leave blank)
"Authorized redirect URIs": http://localhost:3000/accounts/google/login/callback/

Note: During OAuth, strict browser security settings may cause the OAuth flow to error. If so, try setting the authorizing browser to Chrome and removing strict browser security settings.

### Docker

Open a terminal at the project root.

Create local Docker build:

```shell
docker compose -f docker-compose.local.yml build
```

Run the docker local dev build by running:

```shell
docker compose -f docker-compose.local.yml up
```

To run in a detached (background) mode, just:

$ docker compose up -d

These commands don’t run the docs service. In order to run docs service you can run:

$ docker compose -f docker-compose.docs.yml up

To run the docs with local services just use:

$ docker compose -f docker-compose.local.yml -f docker-compose.docs.yml up

The site should start and be accessible at http://localhost:3000

Do:

```shell
docker compose -f docker-compose.local.yml run --rm django python manage.py migrate
docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser
docker compose -f docker-compose.local.yml run --rm django python manage.py startapp gdrivecrud
```

For each OAuth based provider, either add a SocialApp (socialaccount app) containing the required client credentials, or, make sure that these are configured via the SOCIALACCOUNT_PROVIDERS[<provider>]['APP'] setting (see example above).

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

### Custom Bootstrap Compilation

The generated CSS is set up with automatic Bootstrap recompilation with variables of your choice.
Bootstrap v5 is installed using npm and customised by tweaking your variables in `static/sass/custom_bootstrap_vars`.

You can find a list of available variables [in the bootstrap source](https://github.com/twbs/bootstrap/blob/v5.1.3/scss/_variables.scss), or get explanations on them in the [Bootstrap docs](https://getbootstrap.com/docs/5.1/customize/sass/).

Bootstrap's javascript as well as its dependencies are concatenated into a single file: `static/js/vendors.js`.
