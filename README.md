# django-docker-compose-skeleton

This repository serves as a django project skeleton. It includes

- An /auth endpoint to login, register and authenticate users
- An /users endpoint to create, update, retrieve and delete users. Also email and password can be changed.
- It uses three groups: customer, staff and business owner
- It is documented at /api with a OpenAPI schema

## TODO
- Add register email verification
- Add change email verification
- Add GraphQL

## Installation

First install the dependencies to get started:

- Docker
- Python
- An editor like PyCharm

Clone the repository to your device & cd into it

`git clone git@github.com:eBrain-DevOps-Team/vet-portal-api.git`

`cd vet-portal-api`


Get all branches

`git fetch`


Switch to your preferred branch. Keep in mind that master and staging should not be used for development purposes.

`git checkout dev`

## Start up

Create a ".env" file and add the environment variables. The dev .env should look like this:

```
DEBUG=1
POSTGRES_DB=ebrainapi
POSTGRES_USER=api
POSTGRES_PASSWORD=api_pwd
SECRET_KEY=test_key
```

If you prefer different credentials, please also update the docker-compose.yaml file.


Build and pull all necessary dependencies

`docker-compose build`


The API can be started in developent mode. Simply start docker-compose. It will watch all files and restart automatically.

`docker-compose up -d`

### Django setup

Setup django environment and create a superuser

`docker-compose exec web  /bin/sh`

`python manage.py collectstatic --noinput`

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py createsuperuser`

Now Django is set up can be reached via localhost:8000/api/admin


### Django add required data

After the sign up, one has to log in to the admin panel. The admin panel is the Dashboard for the eBrain team.
Here we can find all objects that are stored in our database. To set up the whitelabeled API we first have to create
several objects:

- Company
- Whitelabel
- Address


## Contribution

Please create a new branch and name it like the feature you would like to add.

`git checkout -b feature/login`

When you are ready open a merge request to merge into dev
