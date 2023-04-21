#!/bin/bash

# start containers
docker compose up & disown

sleep 40

# setup the database
commands=`cat dbsetup.sql`
docker exec mysql-database bash -c "mysql -uprod -psomething_encrypt3d ip -e \"${commands}\""

# check that everything works
docker exec mysql-database bash -c "mysql -uprod -psomething_encrypt3d ip -e \"DESC LOGIN_DETAILS;\""
docker exec mysql-database bash -c "mysql -uprod -psomething_encrypt3d ip -e \"DESC MEDIC_DETAILS;\""