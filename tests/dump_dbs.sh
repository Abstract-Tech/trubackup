#!/bin/sh

DIR=$(dirname "$(readlink -f "$0")")
. ${DIR}/variables.sh

# Prepare aliases for the scripts we'll run
alias mysql='docker exec mysql mysql'
alias mongo='docker exec mongo mongo'


# Run the scripts
. ${DIR}/insert_mongo_test_data.sh
. ${DIR}/insert_mysql_test_data.sh

# Dump the databases to the workspace
# TODO
