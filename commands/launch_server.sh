#!/bin/zsh

# to store spwned processes IDs
declare -a pids

# on exit kill the spwned processes
cleanup() {
  for pid in "${pids[@]}"; do
    echo "Killing server process with PID ${pid}"
    kill -9 "$pid"
  done
}
trap "cleanup" INT SIGTERM SIGQUIT

# run server
export FLASK_APP=../be/server/server.py
FLASK_ENV='development' FLASK_DEBUG=1 flask run --no-reload &
pids+=("$!")
echo $pids
wait