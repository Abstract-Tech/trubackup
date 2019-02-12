FROM python:3.6-alpine as builder
# Run with
# docker run registry.abzt.de/edx-backup edxbackup

RUN pip install -U pip
COPY egg /egg
RUN pip install /egg

CMD /usr/local/bin/edxbackup
