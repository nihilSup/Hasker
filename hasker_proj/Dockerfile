FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
COPY . /opt/hasker_proj/
WORKDIR /opt/hasker_proj
RUN pip install -r requirements.txt
ENTRYPOINT [ "/opt/hasker_proj/entrypoint.sh" ]
CMD ["uwsgi", "--ini", "/opt/hasker_proj/uwsgi.ini"]