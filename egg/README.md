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

Restore example:

    docker run --network tutor_local_default -v $(pwd)/tum-dump/mongodump.tar.gz:/tmp/mongodump.tar.gz --rm -ti registry.abzt.de/edx-backup edxbackup mongo_restore --mongo-host mongodb --input-file /tmp/mongodump.tar.gz

TODO: more examples and details
