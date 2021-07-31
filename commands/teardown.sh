#!/bin/bash

PGPASSWORD=1234 psql -U postgres -h 127.0.0.1 -d postgres -c "DROP DATABASE tg_main;"
PGPASSWORD=1234 psql -U postgres -h 127.0.0.1 -d postgres -c "DROP DATABASE tg_test;"
PGPASSWORD=1234 psql -U postgres -h 127.0.0.1 -d postgres -c "DROP ROLE tokengallerist;"

