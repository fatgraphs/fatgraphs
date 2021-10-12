# TokenGallery Map

## Conventions

Case: camelCase everywhere possible. Since snake_case is the ocnvention in python we won't use cameCase in python code.

## Set Up
You need to have `npm` installed.

You need a graph.csv file inside data (currently it needs to be called `medium.csv`)

We use rapids libraries, the easiest way to install is to create an Anaconda
environment
with the command that matches
your specs, generate the command at the following url: https://rapids.ai/start.html
To find out your cuda version conider using the command `nvidia-smi`.
Python version should be python 3.8

The following command should work on Ubuntu 20:

<code>
conda create -n rapids-21.08 -c rapidsai -c nvidia
-c conda-forge -c anaconda rapids=21.08 python=3.8
cudatoolkit=11.2 flask flask-restx flask-cors flask_accepts
geopandas graph-tool marshmallow matplotlib numpy pandas
pillow psycopg2 pytest scikit-image sqlalchemy geoalchemy2 mypy_extensions
</code>

We will now assume that an Anaconda virtual environment called `rapids-21.08`
exists in your system (you can call it something else).

Since some packages are not hosted by any Anaconda channels and the tests
perform image comparisons between an output and a desired model, we need to have
the open-cv library. You can install it with
`pip install opencv-python`
We also use flask_accepts for input/output validation on the server endpoints.
`pip install flask_accepts`

### Tests
To run the `tile_creator` tests you need to have the folder `be/tile_creator/test/data` populated with the appropriate files.
Since those are heavy images and  csv files they have not been commited to te repo.
Ask the project maintainer to provide them to you.

The server tests shouldn't need anything.

#### Run tests as pre-push hook
Copy-paste the below snippet into .git/hooks/pre-push in order to have tests automatically run before each push.
```
#!/bin/bash

remote="$1"
url="$2"
source activate rapids2
export FLASK_ENV='test'
cd ~/tokengallery/be && python -m pytest
```

### Postgres & PostGIS installation
To run the code locally please make sure postgres and the GIS extension are
correctly set up. This was tested with Ubuntu 20.

Ubuntu 20 comes with postgres already installed. Refer to this image to know
what postgres-related paackages are required:
[Postgres-related packages required for this project](docs/postgres_related_packages.png)

Launch a session and set the password for the `postgres` user.
`sudo -u postgres psql`
Set the password to something:
`ALTER USER postgres PASSWORD '1234';`
quit the session.

Launch another session with the postgres user to check that it worked:
`psql -U postgres -h 127.0.0.1`

Quit the session and install the GIS extension.
`sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable`
`sudo apt-get update`
`sudo apt-get install postgis postgresql-postgis-scripts`

To check that it worked, let's launch a new session and add the GIS extension to the deafult database:
```
psql -U postgres -h 127.0.0.1
CREATE EXTENSION POSTGIS;
```
If you now issue a `\dt` command you should see a spatial table that was create.

### Local DB set-up
The configuration of the local db is done by settings the relevant variables in be/configuration.py.
The defaults are a postgres db called `test`, reachable via localhost by a user called 'postgres' with password 1234.
You can overwrite those default to match you system configuration by changing the relevant variables in be/configuration.py

Launch a psql session with your desired username and issue the following command:
`CREATE DATABASE test; (or your chosen db name)`
Switch to the newly created db with:
`\connect test (or your chosen db name)`
Install the extension:
`CREATE EXTENSION POSTGIS;`

Run `labels_ingestion.py` to put a table with the provided labels and types into the above-created database.
The script `labels_ingestion.py` takes as argument a path to the csv file with the labels, check the code of `labels_ingestion.py`
to see what are the required columns.

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

### GTM script- generate token map
The server mainly servers the tiles that make up a map that represents the graph.
The client let you visualise and expolore such map.

But how are the tiles generated?
You need to run `./gtm.py ` from the root of the project, in a terminal where the correct environment is active.
The gtm command takes the following long list of argumeents, but you don't need to specify everything as sensible defaults are in place.
|ARGUMENT FLAG|DESCRIPTION|
|----------|--------|
|-n                         |The name of the generated output. This will also be the name of the folder that wil contain all the genrated tiles.|
|--csv                      |Path to .csv file that contains the graph. The columns of the csv are: source, target, amount. An example of a row of such csv is: `0x88e2efac3d2ef957fcd82ec201a506871ad06204,0x67fa2c06c9c6d4332f330e14a66bdf1873ef3d2b,       1000000000000000000`|
|--labels                   |Path to .csv file with the following columns: type,address,label. An example of a row of such csv is: `airswap,0x7eeab4f134fcfa6fcaf3987d391f1d626f75f6e1, AirSwap: Deployer`|
|--ts                       |The tile size in pixel.|
|-z                         |How many zoom levels the map has. The minimum is 0, meaning the map has one zoom level. Note the for `z= n` 2**n tiles have to rendered.|
|--min_t                    |Minimum transparency for edges. |
|--max_t                    |Maximum transparency for edges. |
|--mean_t                   |This argument is a percentage of the graph side (the graph size is the length of the side of the square that contains the graph). This percentage controls where the gaussian for the edge transparency is centered.|
|--std                      |This argument is a percentage of the graph side. It controls the standard deviation of the the gaussian for the edge transparecy.|
|--max_thick                |The max thickness allowed for edges.|
|--med_thick                |The desired median value for edge thickness.|
|--max_size                 |The max size allowed for vertices.|
|--med_size                 |The desired median size for vertices.|
|--curvature                |Between 0.1 and 1. How curved edges should be.|

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

# MACOS setup
This details the installation steps on macos big sur 11.
Please note that the target machine did not have a GPU compatibe
with CUDA, therefore this set-up is only relevant for running
the FE and the server.

## Postgres
Use the postgres app: https://postgresapp.com/
It contains the postgis extension by default.

CREATE ROLE tokengallerist LOGIN PASSWORD '1234';
GRANT pg_read_server_files TO tokengallerist;

Create a a db called tg_main.
Open a cmd connected to the tg_main db.
Load the dump: `\i ~/tg_main_dump.pgsql` wait until it loads.


Make a conda env with required dependencies:
`conda create -n macEnv -c conda-forge -c anaconda flask flask-restx flask-cors geopandas graph-tool marshmallow matplotlib numpy pandas pillow psycopg2 pytest scikit-image sqlalchemy geoalchemy2 mypy_extensions`
Additionally, add this as well:
`pip install flask_accepts`