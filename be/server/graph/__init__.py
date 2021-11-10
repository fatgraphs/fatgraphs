from flask_admin.contrib.sqla import ModelView

from .model import Graph  # noqa
from .schema import GraphSchema  # noqa
from .. import admin, SessionLocal

BASE_ROUTE = "graph"


def register_routes(api, app):
    from .controller import api as user_api
    root = app.config['API_ROOT']
    api.add_namespace(user_api, path=f"/{root}/{BASE_ROUTE}")
    # make the graphs accessible via the flask admin interface
    admin.add_view(ModelView(Graph, SessionLocal()))


