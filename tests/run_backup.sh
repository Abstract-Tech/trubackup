#!/bin/bash

DESTINATION=$1
IMAGE=$2
DIR=$(dirname "$(readlink -f "$0")")

echo Dumping into ${DESTINATION} using ${IMAGE}

docker run --network host --rm \
    -u $(id -u ${USER}):$(id -g ${USER}) \
    --mount type=bind,source=${DESTINATION},destination=/dumps \
    --mount type=bind,source=${DIR}/../egg,destination=/egg \
    ${IMAGE} \
        edxbackup edx_dump \
            --edx-config /egg/edxbackup/tests/lms.auth.json\
            --dump-location /dumps
