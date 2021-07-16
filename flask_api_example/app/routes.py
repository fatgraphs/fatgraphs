def register_routes(api, app, root="api"):
    from app.user import register_routes as attach_user
    from app.graph import register_routes as attach_graph
    from app.vertex import register_routes as attach_vertex
    from app.metadata import register_routes as attach_metadata
    from app.tile import register_routes as attach_tile


    # Add routes
    attach_user(api, app)
    attach_graph(api, app)
    attach_vertex(api, app)
    attach_metadata(api, app)
    attach_tile(api, app)
    # attach_fizz(api, app)
    # attach_other_api(api, app)
    # app.register_blueprint(create_bp(), url_prefix="/third_party")
