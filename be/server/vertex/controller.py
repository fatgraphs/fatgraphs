from flask import (
    Response,
    request,
)
from flask_accepts import responds
from flask_restx import (
    Namespace,
    Resource,
)

from be.server.server import SessionLocal
from be.server.utils import iterate_stream

from .model import Vertex
from .schema import VertexSchemaPointConversion
from .service import VertexService

api = Namespace("Vertex", description="Single namespace, single entity")  # noqa


@api.route("/closest/<string:graph_id>/<float(signed=True):x>/<float(signed=True):y>")
@api.param("graph_id", "Graph Id")
@api.param("y", "Y coordinate")
@api.param("x", "X coordinate")
class GetClosestVertexWithMetadata(Resource):

    @responds(schema=VertexSchemaPointConversion)
    def get(self, graph_id: int, x: float, y: float) -> Vertex:
        with SessionLocal() as db:
            closest_vertex = VertexService.get_closest(graph_id, x, y, db)
            metadata = VertexService.attach_metadata(closest_vertex, db)
            return metadata[0]


@api.route("/type/<string:type>")
@api.param("type", "type")
class GetVerticesByType(Resource):
    @api.doc(params={'graphId': {'description': 'If you provide a graph id your query will be scoped to that graph only',
                                 'type': 'int'}})
    @responds(schema=VertexSchemaPointConversion(many=True))
    def get(self, type: str) -> Vertex:
        with SessionLocal() as ses:
            graph_id = request.args.get('graphId')
            vertices = VertexService.get_by_type(graph_id, type, ses)
            vertices = VertexService.attach_metadata(vertices, ses)
            return vertices


@api.route("/label/<string:label>")
@api.param("label", "label")
class GetVerticesByLabel(Resource):
    @api.doc(params={'graphId': {'description':  'If you provide a graph id your query will be scoped to that graph only',
                                 'type': 'int'}})
    @responds(schema=VertexSchemaPointConversion(many=True))
    def get(self, label: str) -> Vertex:
        with SessionLocal() as db:
            graph_id = request.args.get('graphId')
            vertices = VertexService.get_by_label(graph_id, label, db)
            vertices = VertexService.attach_metadata(vertices, db)
            # if graph_id is not None:
            #     vertices = VertexService.attach_position(vertices, graph_id, db)
            return vertices

@api.route("/vertex/<string:vertex>")
@api.param("vertex", "Ethereum address")
class GetVerticesByEth(Resource):
    @api.doc(params={'graphId': {'description':  'If you provide a graph id your query will be scoped to that graph only',
                                 'type': 'int'}})
    @responds(schema=VertexSchemaPointConversion(many=True))
    def get(self, vertex: str) -> Vertex:
        with SessionLocal() as db:
            graph_id = request.args.get('graphId')
            vertices = VertexService.get_by_ext_id(graph_id, [vertex], db)
            vertices = VertexService.attach_metadata(vertices, db)
            return vertices

@api.route('/upload')
class UploadVertices(Resource):

    def post(self):
     
        count = 0

        with SessionLocal() as db:
            for vertex in iterate_stream(request):
                vertex = vertex.decode()
                vertex = vertex.split(",")
            
                v = Vertex(
                    graph_id=vertex[0],
                    vertex=vertex[1],
                    size=vertex[2],
                    pos=vertex[3].strip(),
                )
                db.add(v)
                count += 1
                
            db.commit()
            db.flush()

        print("Added ", count, " vertices")

        return Response(status=200)