# TokenGallery Map 
### Set Up
You need to have `npm` installed.

Create an Anaconda environment with the command that matches your specs, generate the command at the following url:
https://rapids.ai/start.html

We will now assume that an Anaconda virtual environment called `rapids-0.18` exists in your system (you can call it something else).

Run `conda install -n rapids-0.18 flask`

Your virtual environment should have all the required packages given that default anaconda environments come with many of the libraries we need pre-installed. If you notice that something is missing please use conda install to add the missing package to the venv.
### Running
#### Activate the venv
Activate the virtual environment (either with the command `conda activate rapids-0.18` or from the anaconda-navvigator UI). 
Alternatively if you are usng a Jetbrain IDE you can set the python interpreter of the project to the be the anconda environment: settings>project:<your_project_name>> drop down menu on python interpreter box > show all > plus icon (+) > conda environment. In this way you can work without leaving the IDE.
#### Launching
`bash launch.sh` should be the only command you need to run to launch both the server and the frontend.
The script launches the Flask server (localhost, default port), does a npm install and launches the map client (react app) which should automatically open up in your broswer
