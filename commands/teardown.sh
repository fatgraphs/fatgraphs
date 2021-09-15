#!/bin/zsh
echo "You are about to drop all databases and users created by the application."
vared -p "Enter password of the postgres user" -c postgres_password

PGPASSWORD=$postgres_password psql -U postgres -h 127.0.0.1 -d postgres -c "DROP DATABASE tg_main;"
PGPASSWORD=$postgres_password psql -U postgres -h 127.0.0.1 -d postgres -c "DROP DATABASE tg_test;"
PGPASSWORD=$postgres_password psql -U postgres -h 127.0.0.1 -d postgres -c "DROP ROLE tokengallerist;"

