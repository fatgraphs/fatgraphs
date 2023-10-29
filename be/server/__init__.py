import os

from flask import Flask, jsonify
from flask_admin import Admin
from flask_cors import CORS
# from vertexObjectlalchemy import SQLAlchemy
from flask_restx import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from werkzeug.routing import IntegerConverter
# from be.server import base_config_flask

# db = SQLAlchemy()
# from be.server.config import config_by_name

# env = os.getenv("FLASK_ENV") or "test"
# configs = config_by_name[env]

Base = declarative_base()


class SignedIntConverter(IntegerConverter):
    regex = r'-?\d+'


def create_app(env=None):
    from be.server.routes import register_routes

    app = Flask(__name__)

    admin = Admin(name='Token Gallery admin panel')
    admin.init_app(app)

    app.config.from_object("be.server.base_config_flask")
    app.config.from_envvar("YOURAPPLICATION_SETTINGS")

    uri = app.config['SQLALCHEMY_DATABASE_URI']

    # engine is the interface-object to interact with DB
    engine = create_engine(uri, echo=True)

    # session is the holding place of ORM objects
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

    cors = CORS(app)
    app.url_map.converters['signed_int'] = SignedIntConverter
    api = Api(app, title="Token Gallery 2.0 API", version="0.1.0")

    register_category_admin_page(admin, SessionLocal)

    # db.init_app(server)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app, SessionLocal, api


def register_category_admin_page(admin, SessionLocal):
    from be.server.admin_setup import do_setup
    do_setup(admin, SessionLocal)


