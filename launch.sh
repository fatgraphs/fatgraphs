#!/bin/bash

declare -a pids
cwd=$(pwd)

cleanup() {
    for pid in "${pids[@]}"; do
        kill -9 "$pid"
    done
}
trap "cleanup" SIGINT SIGTERM

# run server
cd be/tile_server && export FLASK_APP=server.py
flask run &
pids+=("$!")

echo $cwd
echo "$pids"

# run client
cd $cwd
cd fe/map_client && npm i
npm run start
pids+=("$!")

echo "$pids"