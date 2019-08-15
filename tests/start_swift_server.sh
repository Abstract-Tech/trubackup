#!/bin/sh

if ! (docker ps |grep \ keystone$); then
    docker run -d --rm  -p 5000 -p 35357:35357 -p 8080:8080 --name keystone jeantil/openstack-keystone-swift:pike

    while ! docker logs keystone |grep Starting\ object-server...; do
        sleep 0.1
    done
    docker exec keystone /swift/bin/register-swift-endpoint.sh http://127.0.0.1:8080
fi
