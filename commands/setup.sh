#!/bin/zsh

echo "Setup needs to create the tokengallerist user."

vared -p "Enter password of the postgres user" -c postgres_password

vared -p "Enter the IP of the db server, press enter to default to localhost" -c db_ip_address
db_ip_address="${db_ip_address:=127.0.0.1}"

vared -p "Enter password for tokengallerist user, press enter to default to 1234" -c tokengallerist_password
tokengallerist_password="${tokengallerist_password:="1234"}"

PGPASSWORD=$postgres_password psql -U postgres -h $db_ip_address -d postgres -v v1="'${tokengallerist_password}'" -f scripts/create_user.sql



# create db for tests if it doesnt exist
PGPASSWORD=$postgres_password psql -U postgres -h 127.0.0.1 -d postgres -c "SELECT 1 FROM pg_database WHERE datname = 'tg_test'" | \
        grep -q 1 || psql -U postgres -h 127.0.0.1 -f scripts/create_testdb.sql

# create db for main application if it doesnt exist
PGPASSWORD=$postgres_password psql -U postgres -h 127.0.0.1 -d postgres -c "SELECT 1 FROM pg_database WHERE datname = 'tg_main'" | \
        grep -q 1 || psql -U postgres -h 127.0.0.1 -f scripts/create_maindb.sql

# add POSTGIS for geometry columns
PGPASSWORD=$postgres_password psql -U postgres -h 127.0.0.1 -d tg_test -c "CREATE EXTENSION IF NOT EXISTS POSTGIS;"
PGPASSWORD=$postgres_password psql -U postgres -h 127.0.0.1 -d tg_main -c "CREATE EXTENSION IF NOT EXISTS POSTGIS;"

# create tables
PGPASSWORD=$tokengallerist_password psql -U tokengallerist -h 127.0.0.1 -d tg_main -f scripts/create_tables.sql

metadateInitFile=($(python ./scripts/print_vertex_metadata_home.py))
eval "METADATA_VERTEX_INIT_HOME=($metadateInitFile)"

echo "Loading vertex metadata initialisation CSV located at ${METADATA_VERTEX_INIT_HOME}."
PGPASSWORD=$tokengallerist_password psql -U tokengallerist -h 127.0.0.1 -d tg_main -v v1=\'${METADATA_VERTEX_INIT_HOME}\' -f scripts/load_vertex_metadata_init.sql

echo 'Done'
