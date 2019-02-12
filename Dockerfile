FROM python:3.6-alpine as builder

RUN apk add mongodb-tools mariadb-client

RUN pip install -U pip
COPY egg /egg
RUN pip install /egg

CMD /usr/local/bin/edxbackup
