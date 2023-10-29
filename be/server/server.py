import os

from be.server import create_app
from be.server.routes import register_routes
if os.getcwd().split(os.sep)[-1] == "commands":
    # if it's run from the commands frolder then set woring dir to be root
    os.chdir(os.path.abspath(".."))

app, SessionLocal, api = create_app(os.getenv("FLASK_ENV") or "test")
register_routes(api, app)

if __name__ == "__main__":
    app.run(debug=True)
