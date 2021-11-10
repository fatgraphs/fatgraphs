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

    class GraphAdminView(ModelView):
        column_display_pk = True  # optional, but I like to see the IDs in the list
        column_hide_backrefs = False
        column_list = ('id', 'graph_name', 'vertices', 'edges', 'graph_category')

    admin.add_view(GraphAdminView(Graph, SessionLocal()))


