#!/bin/bash

dburl=127.0.0.1
password=1234

# create user
PGPASSWORD=$password psql -U postgres -h $dburl -d postgres -f create_user.sql

# create db for tests if it doesnt exist
psql -U postgres -h 127.0.0.1 -d postgres -c "SELECT 1 FROM pg_database WHERE datname = 'tg_test'" | \
        grep -q 1 || psql -U postgres -h 127.0.0.1 -f create_testdb.sql

# create db for main application if it doesnt exist
psql -U postgres -h 127.0.0.1 -d postgres -c "SELECT 1 FROM pg_database WHERE datname = 'tg_main'" | \
        grep -q 1 || psql -U postgres -h 127.0.0.1 -f create_maindb.sql

# add POSTGIS for geometry columns
psql -U postgres -h 127.0.0.1 -d tg_test -c "CREATE EXTENSION IF NOT EXISTS POSTGIS;"
psql -U postgres -h 127.0.0.1 -d tg_main -c "CREATE EXTENSION IF NOT EXISTS POSTGIS;"

# create tables
PGPASSWORD=$password psql -U tokengallerist -h 127.0.0.1 -d tg_main -f create_tables.sql

# load labels
LABELS_HOME=$(python ./print_labels_home.py)
ACCOUNT_TYPE_HOMES=($(python ./print_account_type_home.py | tr -d '[],'))

echo "Loading labels located at: $LABELS_HOME ..."
PGPASSWORD=$password psql -U tokengallerist -h 127.0.0.1 -d tg_main -v v1="'$LABELS_HOME'" -f load_labels.sql

echo "Loading account types located at ${ACCOUNT_TYPE_HOMES[0]} and ${ACCOUNT_TYPE_HOMES[1]}..."
PGPASSWORD=$password psql -U tokengallerist -h 127.0.0.1 -d tg_main -v v1="${ACCOUNT_TYPE_HOMES[0]}" -f load_account_types.sql
PGPASSWORD=$password psql -U tokengallerist -h 127.0.0.1 -d tg_main -v v1="${ACCOUNT_TYPE_HOMES[1]}" -f load_account_types.sql
psql -U postgres -h 127.0.0.1 -d tg_main -c "CREATE INDEX IF NOT EXISTS vertex_id ON tg_account_type (vertex);"

echo 'Done'