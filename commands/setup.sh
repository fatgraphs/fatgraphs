#!/bin/bash

dburl=127.0.0.1
metadata_ingestion_script=metadata_ingestion.sql
labels_csv_path=../be/data/labels.csv
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

echo "Preparing $metadata_ingestion_script from $labels_csv_path"
python prepare_metadata_ingestion_script.py $labels_csv_path $metadata_ingestion_script

echo 'Ingesting metadata...'
PGPASSWORD=$password psql -U tokengallerist -h 127.0.0.1 -d tg_main -f $metadata_ingestion_script >/dev/null
rm $metadata_ingestion_script
echo 'Done'