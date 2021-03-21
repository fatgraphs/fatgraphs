#!/bin/bash

# to store spwned processes IDs
declare -a pids

# on exit kill the spwned processes
cleanup() {
  echo "Killing"
    for pid in "${pids[@]}"; do
        kill -9 "$pid"
    done
}
trap "cleanup" SIGINT SIGTERM SIGQUIT

#generate tiles
PYTHONPATH=$(pwd) python be/tile_creator/src/main.py

cd fe/map_client
# npm i
npm run webpack
npm run start &
pids+=("$!")
wait # if we dont wait the trap wont work