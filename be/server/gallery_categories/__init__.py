from .model import GalleryCategory  # noqa
from .schema import GalleryCategorySchema  # noqa

BASE_ROUTE = "gallery_categories"


def register_routes(api, app):
    from .controller import api as user_api
    root = app.config['API_ROOT']
    api.add_namespace(user_api, path=f"/{root}/{BASE_ROUTE}")

