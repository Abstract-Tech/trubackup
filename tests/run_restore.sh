#!/usr/bin/env bash
#
set -ex

SOURCE=$1
DIR=$(dirname "$(readlink -f "$0")")
BUILD_IMAGE=$(cat "${DIR}"/../build-image)

# I would like to have --wait flag here but for some obscure reason it does not work in GitHub Actions
docker-compose -f "${DIR}/docker-compose.yml" up -d --force-recreate

# So here's the ugly solution
sleep 10

echo Restoring from ${SOURCE} using ${BUILD_IMAGE}

# Wait for mysql
docker run --network=host jwilder/dockerize:0.6.1 -wait tcp://localhost:3306

# Wait for mongo
docker run --network=host jwilder/dockerize:0.6.1 -wait tcp://localhost:27017

docker run --network host --rm \
    -u $(id -u ${USER}):$(id -g ${USER}) \
    --mount "type=bind,source=${SOURCE},destination=/destination" \
    --mount "type=bind,source=${DIR}/dump_conf.json,destination=/etc/edxbackup.json" \
    "${BUILD_IMAGE}" \
        edxbackup edx_restore

. ${DIR}/.env

MONGO_OPTS="-u ${MONGO_USER} -p${MONGO_PASSWORD} --authenticationDatabase admin"

COUNT=$(docker-compose -f "${DIR}"/docker-compose.yml exec -T mongo mongo test ${MONGO_OPTS} --eval 'db.inventory.count()' | tail -n1)
if [ "${COUNT}" != "3" ]; then
	echo Wrong number of records in mongodb: ${COUNT}
	exit 1
fi
