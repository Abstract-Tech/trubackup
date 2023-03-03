#!/bin/sh

DIR=$(dirname "$(readlink -f "$0")")

while ! docker-compose -f "${DIR}"/docker-compose.yml logs keystone-swift | grep 'Starting object-server...'; do
    sleep 0.1
done
