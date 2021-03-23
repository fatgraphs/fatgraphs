#!/bin/bash

# to store spwned processes IDs
declare -a pids

# on exit kill the spwned processes
cleanup() {
  echo "Killing the client process"
    for pid in "${pids[@]}"; do
        kill -9 "$pid"
    done
}
trap "cleanup" SIGINT SIGTERM SIGQUIT

cd fe/map_client
# npm i
npm run webpack
npm run start &
pids+=("$!")
wait # if we dont wait the trap wont work