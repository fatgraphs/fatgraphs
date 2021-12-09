import os
import shutil

from flask import flash
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView
from psycopg2._psycopg import AsIs

from .model import Graph  # noqa
from .schema import GraphSchema  # noqa
from .. import admin, SessionLocal
from ...configuration import VERTEX_TABLE_NAME, EDGE_TABLE_NAME, CONFIGURATIONS, TILE_FOLDER_NAME

BASE_ROUTE = "graph"


def register_routes(api, app):
    from .controller import api as user_api
    root = app.config['API_ROOT']
    api.add_namespace(user_api, path=f"/{root}/{BASE_ROUTE}")

    # make the graphs accessible via the flask admin interface
