def register_routes(api, app, root="api"):
    from .graph import register_routes as attach_graph
    from .searches import register_routes as attach_user
    from .vertex import register_routes as attach_vertex
    from .vertex_metadata import register_routes as attach_metadata
    from .tile import register_routes as attach_tile
    from .edge import register_routes as attach_edge
    from .gallery_categories import register_routes as attach_gallery_categories
    from .graph_configuration import register_routes as attach_graph_configuration

    attach_gallery_categories(api, app)
    attach_graph(api, app)
    attach_user(api, app)
    attach_vertex(api, app)
    attach_metadata(api, app)
    attach_tile(api, app)
    attach_edge(api, app)
    attach_graph_configuration(api, app)

