#!/bin/sh


mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "CREATE DATABASE test"
STATEMENT="CREATE TABLE pet (name VARCHAR(20), owner VARCHAR(20),
       species VARCHAR(20), sex CHAR(1), birth DATE, death DATE);"
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "${STATEMENT}" test
STATEMENT="INSERT INTO pet
       VALUES ('Puffball','Diane','hamster','f','1999-03-30',NULL);"
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "${STATEMENT}" test
