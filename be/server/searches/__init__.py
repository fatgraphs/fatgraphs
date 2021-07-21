from be.server.searches.model import SearchTerm

BASE_ROUTE = "searches"
AUTOCOMPLETE_TERMS_PER_PAGE = 200

def register_routes(api, app):
    from .controller import api as user_api

    root = app.config['API_ROOT']

    api.add_namespace(user_api, path=f"/{root}/{BASE_ROUTE}")
