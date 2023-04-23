#!/bin/bash

GREEN=$(tput setaf 2)

# get the dev environment ready
sudo apt-get install libmysqlclient-dev
pip3 install flask flask_mysqldb flask_cors

# start containers
docker compose up -d

# wait for the containers (mysql espacially) to start
sleep 40

# setup the database
commands=`cat dbsetup.sql`
docker exec mysql-database bash -c "mysql -uprod -psomething_encrypt3d ip -e \"${commands}\""

# check that everything works
docker exec mysql-database bash -c "mysql -uprod -psomething_encrypt3d ip -e \"DESC LOGIN_DETAILS;\""
docker exec mysql-database bash -c "mysql -uprod -psomething_encrypt3d ip -e \"DESC MEDIC_DETAILS;\""

echo "${GREEN} Enjoy!"