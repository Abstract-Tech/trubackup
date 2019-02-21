edX Backup
==========

Introduction
------------

Simple utility scripts to dump and restore an Open edX instance.

A docker image can be built with:

    make build-image

Usage
-----

Parameters can be passed either as environment variables or on the command line.

Mongodb restore example:

    docker run --network tutor_local_default -v $(pwd)/tum-dump/mongodump.tar.gz:/tmp/mongodump.tar.gz --rm -ti registry.abzt.de/edx-backup edxbackup mongo_restore --mongo-host mongodb --input-file /tmp/mongodump.tar.gz

Mysql restore example:

    docker run --network tutor_local_default -v $(pwd)/tum-dump/mysql_dump.sql.gz:/tmp/mysql_dump.sql.gz --rm -ti registry.abzt.de/edx-backup edxbackup mysql_restore --mysql-host mysql --mysql-user root --mysql-password FOOBAR --input-file /tmp/mysql_dump.sql.gz


TODO: more examples and details
