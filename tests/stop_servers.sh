#!/bin/sh

DIR=$(dirname "$(readlink -f "$0")")
. ${DIR}/.env

docker-compose down
