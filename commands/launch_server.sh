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
FLASK_ENV='development' FLASK_DEBUG=1 YOURAPPLICATION_SETTINGS='dev_config_flask.cfg' flask run --no-reload --debug &
pids+=("$!")
echo $pids
wait