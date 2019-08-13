#!/bin/bash

SOURCE=$1
IMAGE=$2
DIR=$(readlink -m $(dirname "$(readlink -f "$0")"))

echo Restoring from ${SOURCE} using ${IMAGE}

set -x
docker run --network host --rm \
    --mount type=bind,source=${SOURCE},destination=/destination \
    --mount type=bind,source=${DIR}/restore_conf.json,destination=/etc/edxbackup.json \
    ${IMAGE} \
        edxbackup edx_restore
