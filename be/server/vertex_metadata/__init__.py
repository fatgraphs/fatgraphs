from .model import VertexMetadata # noqa
from .schema import VertexMetadataSchema  # noqa

BASE_ROUTE = "vertex-metadata"


def register_routes(api, app):
    from .controller import api as user_api
    root = app.config['API_ROOT']
    api.add_namespace(user_api, path=f"/{root}/{BASE_ROUTE}")
