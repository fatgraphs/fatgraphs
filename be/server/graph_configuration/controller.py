from flask import request
from flask_accepts import (
    accepts,
    responds,
)
from flask_restx import (
    Namespace,
    Resource,
)

from be.server.server import SessionLocal

from . import (
    GraphConfiguration,
    GraphConfigurationSchema,
)
from .service import GraphConfigurationService

api = Namespace("GraphConfiguration", description="Configurations are the gtm.py paramters used to create the graph map")


@api.route("/")
class GraphConfigurationResource(Resource):        
    @responds(schema=GraphConfigurationSchema(many=False))
    @accepts(schema=GraphConfigurationSchema, api=api)
    def post(self) -> GraphConfiguration:    
        print("graph config running")
        obj = request.parsed_obj
        print("config obj", obj)
        with SessionLocal() as db:

            t = GraphConfigurationService.create(
                obj,
                db,
            )
            return t
        
@api.route("/<int:graph_id>")
@api.param("graph_id", "Graph Id")
class GraphConfigurationIdResource(Resource):

    @responds(schema=GraphConfigurationSchema)
    def get(self, graph_id: int) -> GraphConfiguration:
        with SessionLocal() as db:
            return GraphConfigurationService.get_by_id(graph_id, db)

