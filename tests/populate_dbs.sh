#!/bin/sh

DIR=$(dirname "$(readlink -f "$0")")
. ${DIR}/.env

# Prepare aliases for the scripts we'll run
alias mysql="docker-compose -f ${DIR}/docker-compose.yml exec -T mysql mysql"
alias mongo="docker-compose -f ${DIR}/docker-compose.yml exec -T mongo mongo"

# Run the scripts
. ${DIR}/insert_mongo_test_data.sh
. ${DIR}/insert_mysql_test_data.sh
