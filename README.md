# Hasker - stackoverflow core functionality

## Architecture

web client <-> nginx <-> uWSGI <-> django app <-> postgresql

nginx -

- reverse proxy from port 80 to port 8000 of uWSGI
- serves static and media (need to python manage.py collectstatic)

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
- [ ] Check email notifications
- [x] Rewrite password validation by using forms clean
- [ ] Add messages to creating questions and adding answers. Also add messages when something can't be done
- [x] Implement tests
- [x] Migrate to postgresql
- [ ] Add docker, uWSGI, make from github
- [ ] Add tags autocomplit
- [ ] Refactor admin creation form and userform
- [ ] Implement REST API
- [ ] Add proper logging
- [ ] Change profile view - add preview of current avatar
