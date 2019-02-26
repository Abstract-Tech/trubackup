#!/bin/bash

DESTINATION=$1
IMAGE=$2

echo Dumping into ${DESTINATION} using ${IMAGE}

docker run --network host --rm -ti \
    -v ${DESTINATION}:/dumps \
    -v /home/silvio/Abstract/edx-backup/egg:/egg\
    ${IMAGE} \
        edxbackup edx_dump \
            --edx-config /egg/edxbackup/tests/lms.auth.json\
            --dump-location /dumps
