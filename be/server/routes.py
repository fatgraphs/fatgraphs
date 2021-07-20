def register_routes(api, app, root="api"):
    from .graph import register_routes as attach_graph
    from .user import register_routes as attach_user
    from .vertex import register_routes as attach_vertex
    from .metadata import register_routes as attach_metadata
    from .tile import register_routes as attach_tile

    attach_graph(api, app)
    attach_user(api, app)
    attach_vertex(api, app)
    attach_metadata(api, app)
    attach_tile(api, app)

