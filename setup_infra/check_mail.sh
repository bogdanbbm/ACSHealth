command=`cat check_mail.sql`
docker exec mysql-database bash -c "mysql -uprod -psomething_encrypt3d ip -e \"${command}\""
