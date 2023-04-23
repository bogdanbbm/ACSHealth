#!/bin/bash

docker stop mysql-database backend-container
docker rm mysql-database backend-container
docker volume rm setup_infra_data

/bin/bash ./setup_infra.sh