from flask import request
from flask_accepts import responds, accepts
from flask_restx import Namespace, Resource

from .model import Vertex
from .schema import VertexSchema, VertexSchemaPos
from .service import VertexService
from .. import SessionLocal
from ..metadata.service import MetadataService

api = Namespace("Vertex", description="Single namespace, single entity")  # noqa


@api.route("/closest/<string:graph_id>/<float(signed=True):x>/<float(signed=True):y>")
@api.param("graph_id", "Graph Id")
@api.param("y", "Y coordinate")
@api.param("x", "X coordinate")
class VertexClosestResource(Resource):

    @responds(schema=VertexSchemaPos)
    def get(self, graph_id: str, x: float, y: float) -> Vertex:
        with SessionLocal() as db:
            closest_vertex = VertexService.get_closest(graph_id, x, y, db)
            metadata = MetadataService.get_by_eth(closest_vertex.eth, db)
            for m in metadata:
                existing = getattr(closest_vertex, m.meta_type + 's', [])
                existing.append(m.meta_value)
                setattr(closest_vertex, m.meta_type + 's', existing)
            return closest_vertex


@api.route("/by/<int:graph_id>/<string:meta_type>/<string:meta_value>")
@api.param("meta_type", "Type of metadata (e.g. label, type)")
@api.param("meta_value", "Value of the typee (e.g. 'idex', 'dex' or 'Idex: coordinator'")
@api.param("graph_id", "Graph Id")
class VertexTypeValueResource(Resource):

    @responds(schema=VertexSchemaPos(many=True))
    def get(self, meta_type: str, meta_value: float, graph_id: int) -> Vertex:
        with SessionLocal() as db:
            vertices = VertexService.get_matching(graph_id, meta_type, meta_value, db)
            for v in vertices:
                metadata = MetadataService.get_by_eth(v.eth, db)
                for m in metadata:
                    existing = getattr(v, m.meta_type + 's', [])
                    existing.append(m.meta_value)
                    setattr(v, m.meta_type + 's', existing)
            return vertices


@api.route("/create")
class VertexResource(Resource):

    # TODO return confirmation message
    @accepts(schema=VertexSchema(many=True), api=api)
    @responds(schema=VertexSchema(many=True))
    def post(self) -> Vertex:
        with SessionLocal() as db:
            vertices = request.parsed_obj
            graph_id = vertices[0]['graph_id']
            vertex_table_name = VertexService.get_vertex_table_name(graph_id, db)
            VertexService.ensure_table_exists(vertex_table_name, db)
            create = VertexService.create(vertex_table_name, vertices, db)
            db.commit()
            return create