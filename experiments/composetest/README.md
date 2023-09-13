# Demo of how to package fatGraphs in docker compose

The gtm, backend and frontend end up in their separate containers.

GTM creates a sqlite file by using the server as the data access layer (called
via localhost).

Frontend is a web app that asks the server requests.

## How to run a py script that is in a docker container
docker run composetest-gtm python ./gtm.py --can "pass" --arguments "like this"

## How to access frontend
http://localhost:8000/
