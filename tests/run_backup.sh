#!/bin/sh
# This is a mess

set -ex

DESTINATION=$1
DIR=$(dirname "$(readlink -f "$0")")
BUILD_IMAGE=$(cat "${DIR}"/../build-image)

# I would like to have --wait flag here but for some obscure reason it does not work in GitHub Actions
docker-compose -f "${DIR}/docker-compose.yml" up -d  --force-recreate

# So here's the ugly solution
sleep 10

"${DIR}"/populate_dbs.sh

docker run --network host --rm \
    -v "${DIR}/rclone.conf:/config/rclone/rclone.conf" \
    rclone/rclone:1.61 purge test_backup || true

echo Dumping into ${DESTINATION} using ${BUILD_IMAGE}

docker run --network host --rm \
    -u $(id -u ${USER}):$(id -g ${USER}) \
    -v "${DIR}/rclone.conf:/etc/rclone/rclone.conf" \
    --mount type=bind,source=${DESTINATION},destination=/destination \
    --mount type=bind,source=${DIR}/dump_conf.json,destination=/etc/edxbackup.json \
    ${BUILD_IMAGE} \
        edxbackup edx_dump

# Make a couple of assertions about the presence of the backup in minio
OUT=$(docker run --network host --rm \
    -v "${DIR}/rclone.conf:/config/rclone/rclone.conf" \
    rclone/rclone:1.61 ls minio:test-backup)

echo "${OUT}" | grep "test.pet-schema" || false
echo "${OUT}" | grep "mongodb_dump" || false

docker-compose -f "${DIR}/docker-compose.yml" down
