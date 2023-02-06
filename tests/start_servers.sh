#!/bin/sh

set -x

DIR=$(dirname "$(readlink -f "$0")")
. ${DIR}/.env

# Start swift server
${DIR}/start_swift_server.sh

# Wait for mongodb
while ! (docker logs edxbackup_test_mongo|grep "waiting for connections"); do
    sleep 0.2
done

# Wait for mysql
while ! (docker logs edxbackup_test_mysql 2>&1  |grep "starting as process 1"); do
    sleep 0.2
done
