#!/bin/bash

DESTINATION=$1
IMAGE=$2
DIR=$(dirname "$(readlink -f "$0")")
EGG_DIR=$(dirname "$DIR")/egg
echo $EGG_DIR

echo Dumping into ${DESTINATION} using ${IMAGE}

set -x
docker run --network host --rm \
    -u $(id -u ${USER}):$(id -g ${USER}) \
    --mount type=bind,source=${DESTINATION},destination=/destination \
    --mount type=bind,source=${DIR}/dump_conf.json,destination=/etc/edxbackup.json \
    `#--mount type=bind,source=${EGG_DIR},destination=/egg `\
    ${IMAGE} \
        edxbackup edx_dump
