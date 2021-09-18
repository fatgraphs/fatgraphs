import os

from be.server import create_app
if os.getcwd().split(os.sep)[-1] == "commands":
    # if it's run from the commands frolder then set woring dir to be root
    os.chdir(os.path.abspath(".."))
app = create_app(os.getenv("FLASK_ENV") or "test")
if __name__ == "__main__":
    app.run(debug=True)
