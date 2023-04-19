#!/usr/bin/env sh

# --- Init restic repo
restic init

# --- Insert mysql test data
MYSQL_OPTS="--user=${MYSQL_USER} --password=${MYSQL_PASSWORD} --host=localhost --port=13306"

MYSQL_SCRIPT='
CREATE DATABASE test;
USE test;
CREATE TABLE test (name VARCHAR(20), owner VARCHAR(20), species VARCHAR(20), sex CHAR(1), birth DATE, death DATE);
INSERT INTO test VALUES ("Puffbal", "Diane", "hamster", "f", "1999-03-30", NULL);
'
mysql ${MYSQL_OPTS} -e "${MYSQL_SCRIPT}" > /dev/null

# --- Insert mongo test data
MONGO_OPTS="--username=${MONGO_USER} --password=${MONGO_PASSWORD} --host=localhost --port=37017 --authenticationDatabase admin"

MONGO_SCRIPT='
db.disableFreeMonitoring();
db.test.insertOne({ item: "journal", qty: 25, tags: ["blank", "red"], size: { h: 14, w: 21, uom: "cm" } });
db.test.insertOne({ item: "mat", qty: 85, tags: ["gray"], size: { h: 27.9, w: 35.5, uom: "cm" } });
db.test.insertOne({ item: "mousepad", qty: 25, tags: ["gel", "blue"], size: { h: 19, w: 22.85, uom: "cm" } });
'
mongosh test ${MONGO_OPTS} --eval "${MONGO_SCRIPT}" > /dev/null

# --- Insert minio test data
mc mb test/test
echo "foo" | mc pipe test/test/bar > /dev/null
