from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from werkzeug.routing import IntegerConverter

db = SQLAlchemy()


class SignedIntConverter(IntegerConverter):
    regex = r'-?\d+'

def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    cors = CORS(app)
    app.url_map.converters['signed_int'] = SignedIntConverter
    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="Token Gallery 2.0 API", version="0.1.0")

    # there is one flask app
    # there is one REST api
    # there are MANY namespaces in the api

    register_routes(api, app)
    db.init_app(app)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
