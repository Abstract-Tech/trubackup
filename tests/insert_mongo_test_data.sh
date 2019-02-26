#!/bin/sh

if [ ! -z "$MONGO_USER" ] ; then
    MONGO_OPTS="${MONGO_OPTS} -u ${MONGO_USER}"
fi
if [ ! -z "$MONGO_PASSWORD" ] ; then
    MONGO_OPTS="${MONGO_OPTS} -u ${MONGO_PASSWORD}"
fi


SCRIPT='
db.inventory.insert({ item: "journal", qty: 25, tags: ["blank", "red"], size: { h: 14, w: 21, uom: "cm" } });
db.inventory.insert({ item: "mat", qty: 85, tags: ["gray"], size: { h: 27.9, w: 35.5, uom: "cm" } });
db.inventory.insert({ item: "mousepad", qty: 25, tags: ["gel", "blue"], size: { h: 19, w: 22.85, uom: "cm" } });
'
mongo test ${MONGO_OPTS} --eval "${SCRIPT}"
