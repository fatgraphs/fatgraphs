#!/bin/bash

# to store spwned processes IDs
declare -a pids

# on exit kill the spwned processes
cleanup() {
  echo "Killing the server process"
  for pid in "${pids[@]}"; do
    kill -9 "$pid"
  done
}
trap "cleanup" INT SIGTERM SIGQUIT

#generate tiles
# PYTHONPATH=$(pwd) python be/tile_creator/main.py

# run server
export FLASK_APP=be/server/server.py
flask run &
pids+=("$!")
echo $pids
wait