import os

from flask import Flask, jsonify
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS
# from vertexObjectlalchemy import SQLAlchemy
from flask_restx import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from werkzeug.routing import IntegerConverter

# db = SQLAlchemy()
from be.server.config import config_by_name

env = os.getenv("FLASK_ENV") or "test"
configs = config_by_name[env]

uri = configs.SQLALCHEMY_DATABASE_URI
engine = create_engine(uri, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
Base = declarative_base()
admin = Admin(name='Token Gallery admin panel')


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')
admin.add_view(MyView(name='Hello'))

class SignedIntConverter(IntegerConverter):
    regex = r'-?\d+'


def create_app(env=None):
    from be.server.config import config_by_name
    from be.server.routes import register_routes

    app = Flask(__name__)

    admin.init_app(app)
    db = SessionLocal()

    app.config.from_object(config_by_name[env or "test"])
    cors = CORS(app)
    app.url_map.converters['signed_int'] = SignedIntConverter
    api = Api(app, title="Token Gallery 2.0 API", version="0.1.0")

    register_routes(api, app)

    # db.init_app(server)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
