from .model import Graph  # noqa
from .schema import GraphSchema  # noqa

BASE_ROUTE = "graph"


def register_routes(api, app):
    from .controller import api as user_api
    root = app.config['API_ROOT']
    api.add_namespace(user_api, path=f"/{root}/{BASE_ROUTE}")

    # make the graphs accessible via the flask admin interface
