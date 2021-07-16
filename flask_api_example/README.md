# Example of a scalable Flask API

psql -U postgres -h 127.0.0.1 -d test -a -f create_db_tables.sql

psql -U postgres -h 127.0.0.1 -d test -a -f metadata_ingestion.sql >/dev/null