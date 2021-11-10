from flask_admin.contrib.sqla import ModelView

from .model import GraphConfiguration  # noqa
from .schema import GraphConfigurationSchema  # noqa
from .. import admin, SessionLocal

BASE_ROUTE = "graph_configuration"


def register_routes(api, app):
    from .controller import api as user_api
    root = app.config['API_ROOT']
    api.add_namespace(user_api, path=f"/{root}/{BASE_ROUTE}")