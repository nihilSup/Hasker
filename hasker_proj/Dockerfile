FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_ENV=test \
    DJANGO_DB=postgres
COPY . /opt/hasker_proj/
WORKDIR /opt/hasker_proj
RUN pip install -r requirements.txt
CMD ["uwsgi", "--ini", "/opt/hasker_proj/uwsgi.ini"]