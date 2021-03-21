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
trap "cleanup" INT SIGTERM SIGQUIT

# run server
cd be/tile_server && export FLASK_APP=server.py
flask run &
pids+=("$!")
echo $pids
wait