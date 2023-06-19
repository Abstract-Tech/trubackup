FROM python:3.11-slim-bullseye

RUN mkdir /app
WORKDIR /app

ARG mydumper_version=0.14.3-1
ARG mongodb_version=100.7.0
ARG restic_version=0.15.1

ENV MYDUMPER_VERSION=${mydumper_version}
ENV MONGOTOOLS_VERSION=${mongodb_version}
ENV RESTIC_VERSION=${restic_version}

RUN apt-get update && apt-get install -y bzip2 curl postgresql-client-common postgresql-client-13

RUN curl -LO https://github.com/mydumper/mydumper/releases/download/v${MYDUMPER_VERSION}/mydumper_${MYDUMPER_VERSION}-zstd.bullseye_amd64.deb && \
    apt install -y ./mydumper*.deb && rm ./mydumper*.deb

RUN curl -LO https://fastdl.mongodb.org/tools/db/mongodb-database-tools-debian11-x86_64-${MONGOTOOLS_VERSION}.deb && \
    apt install -y ./mongodb-database-tools*.deb && rm ./mongodb-database-tools*.deb

RUN curl -L https://github.com/restic/restic/releases/download/v${RESTIC_VERSION}/restic_${RESTIC_VERSION}_linux_amd64.bz2 | \
	bunzip2 > /usr/local/bin/restic && chmod +x /usr/local/bin/restic

COPY requirements.txt pyproject.toml /app/
COPY edxbackup /app/edxbackup

COPY contrib/delete_old.py /usr/local/bin/delete_old.py

RUN pip install -r /app/requirements.txt && pip install /app
