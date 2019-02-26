#!/bin/bash

SOURCE=$1
IMAGE=$2

echo Restoring from ${SOURCE} using ${IMAGE}

docker run --network host --rm -ti \
    --mount type=bind,source=${SOURCE},destination=/dumps \
    ${IMAGE} \
        edxbackup edx_restore \
            --edx-config /egg/edxbackup/tests/lms.auth.json\
            --dump-location /dumps
