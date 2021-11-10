from flask_accepts import responds
from flask_restx import Namespace, Resource

from . import GraphConfigurationSchema, GraphConfiguration
from .service import GraphConfigurationService
from .. import SessionLocal

api = Namespace("GraphConfiguration", description="Configurations are the gtm.py paramters used to create the graph map")


@api.route("/<int:graph_id>")
@api.param("graph_id", "Graph Id")
class GraphConfigurationIdResource(Resource):

    @responds(schema=GraphConfigurationSchema)
    def get(self, graph_id: int) -> GraphConfiguration:
        with SessionLocal() as db:
            return GraphConfigurationService.get_by_id(graph_id, db)
