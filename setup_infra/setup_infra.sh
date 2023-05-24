
GREEN=$(tput setaf 2)

# get the dev environment ready
sudo apt-get install libmysqlclient-dev
pip install flask flask_mysqldb flask_cors pyjwt flask_sqlalchemy

# start containers
docker compose up -d

echo "${GREEN} Enjoy!"