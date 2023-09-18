from typing import List
from flask import Response, request

from flask_accepts import responds
from flask_restx import Namespace, Resource

from be.server.utils import iterate_stream
from be.server.vertex.model import Vertex

from .model import Edge
from .schema import EdgeSchema
from .service import EdgeService
from .. import SessionLocal

api = Namespace("Edge", description="Single namespace, single entity")  # noqa


@api.route("/<string:graph_id>/<string:vertex>")
@api.param("graph_id", "Graph Id")
@api.param("vertex", "The vertex to query")
class GetEdges(Resource):

    @responds(schema=EdgeSchema(many=True))
    def get(self, graph_id: int, vertex: str) -> List[Edge]:
        with SessionLocal() as db:
            edges = EdgeService.get_edges(vertex, graph_id, db)
            return edges
        
@api.route('/upload')
class UploadEdges(Resource):

    def post(self):
     
        count = 0

        with SessionLocal() as db:
            for edge in iterate_stream(request):
                edge = edge.decode()
                edge = edge.split(",")

                print(">> edge", edge)
                
                v = Edge(
                    graph_id=edge[3].strip(),
                    src=Vertex(vertex = edge[0].strip(), graph_id = edge[3].strip()),
                    trg=Vertex(vertex = edge[1].strip(), graph_id = edge[3].strip()),
                    amount=edge[2].strip(),
                )
                v.add(db)
                count += 1
                
            db.commit()
            db.flush()

        print("Added ", count, " vertices")

        return Response(status=200)

