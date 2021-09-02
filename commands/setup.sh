#!/bin/bash

echo "Setup needs to create the tokengallerist user."

read -p "Enter password of the postgres user " postgres_password

read -p "Enter the IP of the db server, press enter to default to locahost" db_ip_address
db_ip_address="${db_ip_address:=127.0.0.1}"

read -p "Enter password for tokengallerist user, press enter to default to 1234" tokengallerist_password
tokengallerist_password="${tokengallerist_password:="1234"}"

PGPASSWORD=$postgres_password psql -U postgres -h $db_ip_address -d postgres -v v1="'${tokengallerist_password}'" -f scripts/create_user.sql



# create db for tests if it doesnt exist
psql -U postgres -h 127.0.0.1 -d postgres -c "SELECT 1 FROM pg_database WHERE datname = 'tg_test'" | \
        grep -q 1 || psql -U postgres -h 127.0.0.1 -f scripts/create_testdb.sql

# create db for main application if it doesnt exist
psql -U postgres -h 127.0.0.1 -d postgres -c "SELECT 1 FROM pg_database WHERE datname = 'tg_main'" | \
        grep -q 1 || psql -U postgres -h 127.0.0.1 -f scripts/create_maindb.sql

# add POSTGIS for geometry columns
psql -U postgres -h 127.0.0.1 -d tg_test -c "CREATE EXTENSION IF NOT EXISTS POSTGIS;"
psql -U postgres -h 127.0.0.1 -d tg_main -c "CREATE EXTENSION IF NOT EXISTS POSTGIS;"

# create tables
PGPASSWORD=$tokengallerist_password psql -U tokengallerist -h 127.0.0.1 -d tg_main -f scripts/create_tables.sql

# load labels
LABELS_HOME=$(python ./scripts/print_labels_home.py)
ACCOUNT_TYPE_HOMES=($(python ./scripts/print_account_type_home.py | tr -d '[],'))

echo "Loading labels located at: $LABELS_HOME ..."
PGPASSWORD=$tokengallerist_password psql -U tokengallerist -h 127.0.0.1 -d tg_main -v v1="'$LABELS_HOME'" -f scripts/load_labels.sql

echo "Loading account types located at ${ACCOUNT_TYPE_HOMES[0]} and ${ACCOUNT_TYPE_HOMES[1]}..."
PGPASSWORD=$password psql -U tokengallerist -h 127.0.0.1 -d tg_main -v v1="${ACCOUNT_TYPE_HOMES[0]}" -v v2="${ACCOUNT_TYPE_HOMES[1]}" -f scripts/load_account_types.sql
echo "Creating index on account_type table after it has been populated..."
psql -U postgres -h 127.0.0.1 -d tg_main -c "CREATE INDEX IF NOT EXISTS vertex_id ON tg_account_type (vertex);"

echo 'Done'