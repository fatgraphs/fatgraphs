#!/bin/bash

# to store spwned processes IDs
declare -a pids
cwd=$(pwd)

# on exit kill the spwned processes
cleanup() {
  echo "Killing server and client"
    for pid in "${pids[@]}"; do
        kill -9 "$pid"
    done
}
trap "cleanup" SIGINT SIGTERM

#generate tiles
PYTHONPATH=$(pwd) python be/tile_creator/src/main.py

# run server
cd $cwd
cd be/tile_server && export FLASK_APP=server.py
flask run &
pids+=("$!")

# run client
cd $cwd
cd fe/map_client && npm i
npm run start
pids+=("$!")