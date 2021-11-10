import os

from flask import Flask, jsonify, flash
from flask_admin import Admin, BaseView, expose
from flask_admin.babel import gettext
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

    register_category_admin_page()

    # db.init_app(server)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app


def register_category_admin_page():
    from be.server.graph import Graph
    from be.server.gallery_categories import GalleryCategory
    class GraphCategoryView(ModelView):

        def delete_model(self, model):
            """
                Delete model.
                :param model:
                    Model to delete
            """
            try:
                if len(self.session.query(Graph).filter_by(graph_category=model.id).all()) > 0:
                    flash(gettext('Failed to delete. \n'
                                  f'To delete this category ensure there are no graphs of category {model.id}'))
                    return False
                self.on_model_delete(model)
                self.session.flush()
                self.session.delete(model)
                self.session.commit()
            except Exception as ex:
                if not self.handle_view_exception(ex):
                    flash(gettext('Failed to delete record. %(error)s', error=str(ex)), 'error')

                self.session.rollback()

                return False
            else:
                self.after_model_delete(model)

            return True

    admin.add_view(GraphCategoryView(GalleryCategory, SessionLocal()))
