#!/bin/zsh

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

cd ../fe/map_client
# npm i
#export NODE_OPTIONS=--openssl-legacy-provider

# or nvm command not available
source /home/carlo/.nvm/nvm.sh

nvm use 14
npm run webpack
npm run start &
pids+=("$!")
wait # if we dont wait the trap wont work
