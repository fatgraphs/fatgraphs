from .model import User  # noqa
from .schema import UserSchema  # noqa

BASE_ROUTE = "user"


def register_routes(api, app):
    from .controller import api as user_api

    root = app.config['API_ROOT']

    api.add_namespace(user_api, path=f"/{root}/{BASE_ROUTE}")
