# TokenGallery Map 
## Set Up
You need to have `npm` installed.

You need a graph.csv file inside data (currently it needs to be called `medium.csv`)

Create an Anaconda environment with the command that matches your specs, generate the command at the following url:
https://rapids.ai/start.html

We will now assume that an Anaconda virtual environment called `rapids-0.18` exists in your system (you can call it something else).

Run `conda install -n rapids-0.18 flask flask_cors`
Since the tests perform image comparisons between an output and a desired model, we need to have the open-cv library.
This is somewhat problematic to install, please execute the command below on a terminal with the conda environment active.
`pip install opencv-python`

Your virtual environment should have all the required packages given that default anaconda environments come with many of
the libraries we need pre-installed. If you notice that something is missing please use conda install to add the missing 

### Tests
To run the `tile_creator` tests you need to have the folder `be/tile_creator/test/data` populated with the appropriate files.
Since those are heavy images and  csv files they have not been commited. Ask the project maintainer to provide them to you.
#### Run tests as pre-push hook 
Copy-paste the below snippet into .git/hooks/pre-push in order to have tests automatically run before each push.
```
#!/bin/bash

remote="$1"
url="$2"

source activate <name of your python environment>
cd ~/tokengallery/be/tile_creator && python -m pytest
```

### PostGIS installation
To run the code locally please make sure postgres and the GIS extension are correctly set up.
On Ubuntu 20 install with the below:

`apt-get install postgresql-12 postgresql-contrib`

Launch a session and set the password for the `postgres` user.
`sudo -u postgres psql`
`ALTER USER postgres  PASSWORD 1234`

Launch a session with the postgres user to check that it worked:
`psql -U postgres -h 127.0.0.1`

Quit the session and install the GIS extension:
`sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable`
`sudo apt-get update`
finally
`sudo apt-get install postgis`

To check that it worked, let's launch a new session and add the GIS extension to the deafult database:
```
psql -U postgres -h 127.0.0.1
CREATE EXTENSION POSTGIS;
```
If you now issue a `\dt` command you should see a spatial table that was create.

### Local DB set-up
As of now, the gtm.py script needs a postgres db called `test` reachable via localhost.
Create it by launching a psql session and issuing the following command:
`CREATE DATABASE test;`
Switch to the newly created db with:
`\connect test`
Install the extension:
`CREATE EXTENSION POSTGIS;`
You should be ready to go.

#### Postgres useful cmd commands
| Description                                       |Command|
| -----------                                       |-----------|
| To quit the session                               |`\q`|
| Show tables in current db                         |`\d`|
|List columns of a table                            |`\d <table_name>`|
|List databases available in the server             |`\l`|
|Show current database and logged user              |`\c`|
|Change database                                    |`\connect <db_name>`|

## Running
### Activate the venv
Activate the virtual environment (either with the command `conda activate rapids-0.18` or from the anaconda-navvigator UI). 
Alternatively if you are usng a Jetbrain IDE you can set the python interpreter of the project to the be the anconda environment: settings>project:<your_project_name>> drop down menu on python interpreter box > show all > plus icon (+) > conda environment. In this way you can work without leaving the IDE.
### Launching server and client
`bash launch_client.sh` and `bash launch_server.sh`should be the only command you need to run to launch the server 
and the frontend.
### GTM - generate token map
The server mainly servers the tiles that make up a map that represents the graph.
The client let you visualise and expolore such map.

But how are the tiles generated?
You need to run `./gtm.py ` from the root of the project, in a terminal where the correct environment is active.

|ARG FLAG|DESCRIPTION|
|--------|--------|
|-n|        The name of the generated output. This will also be the name of the folder that wil contain all the genrated tiles.|



# Folder Structure
be: backend
fe: frontend
### BE
The tile creator takes a csv of a graph of transactions and generates square tiles at different levels of zoom.
You can change the zoom level as ann argument to the render function.

The tile_server is a flask server responding to requests for tiles. 

### FE
The fronted is a simple react JS application that has a leaflet map.
The map has a tile layer that is instructed to fetch tiles from our tile_server running on localhost.
You can specify how many zooms levels are available on the map by modifying the appropriate 
variable in `fe/map_client/src/components/mymap/configurations.js`.
If you do that remember to update the tile_creator to generate tiles for all the zoom levels.

# Experimetns
This folder contains jupyter notebooks, previous work & experimental code.
