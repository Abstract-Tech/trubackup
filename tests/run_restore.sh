#!/bin/bash

SOURCE=$1
IMAGE=$2
DIR=$(dirname "$(readlink -f "$0")")

echo Restoring from ${SOURCE} using ${IMAGE}

docker run --network host --rm -ti \
    --mount type=bind,source=${SOURCE},destination=/dumps \
    --mount type=bind,source=${DIR}/../egg,destination=/egg \
    ${IMAGE} \
        edxbackup edx_restore \
            --edx-config /egg/edxbackup/tests/lms.auth.json\
            --dump-location /dumps
