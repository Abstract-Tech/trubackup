#!/bin/bash

DESTINATION=$1
IMAGE=$2
DIR=$(dirname "$(readlink -f "$0")")

echo Dumping into ${DESTINATION} using ${IMAGE}

set -x
docker run --network host --rm \
    -u $(id -u ${USER}):$(id -g ${USER}) \
    --mount type=bind,source=${DESTINATION},destination=/dumps \
    --mount type=bind,source=${DIR}/dump_conf.json,destination=/dump_conf.json \
    ${IMAGE} \
        edxbackup edx_dump \
            --dbconfig-path /dump_conf.json \
            --dump-location /dumps
