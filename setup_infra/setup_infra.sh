
GREEN=$(tput setaf 2)

# get the dev environment ready
sudo apt-get install libmysqlclient-dev
pip install flask flask_mysqldb flask_cors pyjwt flask_sqlalchemy

# start containers
docker compose up -d

# wait for the containers (mysql espacially) to start
sleep 30

# setup the database
commands=`cat dbsetup.sql`
docker exec mysql-database bash -c "mysql -uprod -psomething_encrypt3d ip -e \"${commands}\""

# check that everything works
# docker exec mysql-database bash -c "mysql -uprod -psomething_encrypt3d ip -e \"DESC LOGIN_DETAILS;\""
# docker exec mysql-database bash -c "mysql -uprod -psomething_encrypt3d ip -e \"DESC MEDIC_DETAILS;\""
# docker exec mysql-database bash -c "mysql -uprod -psomething_encrypt3d ip -e \"DESC REVIEWS;\""
docker exec mysql-database bash -c "mysql -uprod -psomething_encrypt3d ip -e \"DESC PATIENT_DATA;\""
docker exec mysql-database bash -c "mysql -uprod -psomething_encrypt3d ip -e \"DESC WEIGHT_HISTORY;\""
docker exec mysql-database bash -c "mysql -uprod -psomething_encrypt3d ip -e \"DESC CONSULTATION_LIST;\""
docker exec mysql-database bash -c "mysql -uprod -psomething_encrypt3d ip -e \"DESC BLOOD_DONATION;\""

echo "${GREEN} Enjoy!"