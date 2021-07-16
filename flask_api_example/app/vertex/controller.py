from flask_accepts import responds
from flask_restx import Namespace, Resource

from .model import Vertex
from .schema import VertexSchema
from .service import VertexService

api = Namespace("Vertex", description="Single namespace, single entity")  # noqa


@api.route("/closest/<string:graph_name>/<float(signed=True):x>/<float(signed=True):y>")
@api.param("graph_name", "Graph Name")
@api.param("y", "Y coordinate")
@api.param("x", "X coordinate")
class VertexClosestResource(Resource):

    @responds(schema=VertexSchema)
    def get(self, graph_name: str, x: float, y: float) -> Vertex:
        return VertexService.get_closest(graph_name, x, y)


@api.route("/by/<string:meta_type>/<string:meta_value>/")
@api.param("meta_type", "Type of metadata (e.g. label, type)")
@api.param("meta_value", "Value of the typee (e.g. 'idex', 'dex' or 'Idex: coordinator'")
@api.param("graph_name", "Graph Name")
class VertexTypeValueResource(Resource):

    @responds(schema=VertexSchema(many=True))
    def get(self, meta_type: str, meta_value: float, graph_name: str) -> Vertex:
        return VertexService.get_matching(graph_name, meta_type, meta_value)


@api.route("/create")
@api.param("meta_type", "Type of metadata (e.g. label, type)")
@api.param("meta_value", "Value of the typee (e.g. 'idex', 'dex' or 'Idex: coordinator'")
class VertexTypeValueResource(Resource):

    @responds(schema=VertexSchema(many=True))
    def get(self, meta_type: str, meta_value: float) -> Vertex:
        return VertexService.get_matching(meta_type, meta_value)