#!/bin/sh

DIR=$(dirname "$(readlink -f "$0")")
MYSQL_PASSWORD=foobar
MYSQL_VERSION=5.6.36
MONGO_VERSION=3.2.16
# Start mongo and mysql services
docker run --rm -d --name mysql -e MYSQL_ROOT_PASSWORD=${MYSQL_PASSWORD} mysql:${MYSQL_VERSION}
docker run --rm -d --name mongo mongo:${MONGO_VERSION}

# Prepare aliases for the scripts we'll run
alias mysql='docker exec mysql mysql'
alias mongo='docker exec mongo mongo'


# Run the scripts
# Wait for mongodb
while ! (docker logs mongo|grep "waiting for connections"); do
    sleep 0.2
done

. ${DIR}/insert_mongo_test_data.sh

# Wait for mysql to be ready
while ! (docker logs mysql 2>&1  |grep "starting as process 1"); do
    sleep 0.2
done
. ${DIR}/insert_mysql_test_data.sh


# Dump the databases to the workspace

# Stop the containers
docker stop mongo
# Mysql is slow to stop. We're removing the container anyway,
# so we save some seconds (2 to 10 on my machine) by killing it
docker kill mysql
