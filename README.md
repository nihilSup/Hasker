# Hasker - stackoverflow core functionality

## How to use

To deploy app use

```shell
cd Hasker
docker-compose up --build -V
```

!!! For prod environment you have to set DJANGO_SECRET_KEY !!!

This will deploy all stack on port 8000. One can use `shell docker build . -t web` to launch only django with uWSGI. But it ups to you to configure db.

There are several ENV vars to control the config:

- DJANGO_ENV tells to use prod or debug for django (e.g. static and media files will be handled differently)
- DJANGO_DB can be postgresql or SQLite. Anyway web Dockerfile entrypoint will load basic data to db.
- UWSGI_PORT describes port to start uWSGI server
- DJANGO_SECRET_KEY used for csrf protection. **Must be set** in production

To set them use docker flags or add .env file to the root folder (among docker-compose.yml)

There are several convience things in entrypoint of django uWSGI docker:

- db flush
- db load from fixture
- collect static

## Architecture

web client <-> nginx <-> uWSGI <-> django app <-> postgresql

nginx -

- reverse proxy from port 8000 to internal 80 and then to port 8000 of uWSGI docker
- serves static and media in prod (need to `python manage.py collectstatic`)

uWSGI -

- gets dynamic requests from nginx and call django middleware

django app -

- contains all business logic
- serves dynamic content
- talks to persistance

postgresql -

- persistance

### Usefull links

<https://www.eidel.io/2017/07/10/dockerizing-django-uwsgi-postgres/>
<https://github.com/twtrubiks/docker-django-nginx-uwsgi-postgres-tutorial>
<https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html>
<http://pawamoy.github.io/2018/02/01/docker-compose-django-postgres-nginx.html>
<https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/>

## TODO

- [x] Change arrows up
- [x] Add sorting by votes and date to answers
- [x] Fix login required for doing GET to votes
- [x] Add asked time ago
- [x] Add paging to question view
- [x] Add Vote and Asnwer counters to index
- [x] Add double sorting and paging to index
- [x] Add email notifications of new answers
- [x] Add correct asnwer mark
- [x] Handle tags
- [x] Add search functional
- [x] Add sidebar
- [x] Check email notifications
- [x] Rewrite password validation by using forms clean
- [ ] Add messages to creating questions and adding answers. Also add messages when something can't be done
- [x] Implement tests
- [x] Migrate to postgresql
- [x] Add docker, uWSGI, make from github
- [ ] Add tags autocomplit
- [ ] Refactor admin creation form and userform
- [ ] Implement REST API
- [x] Add logging
- [ ] Change profile view - add preview of current avatar
