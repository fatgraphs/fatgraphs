from typing import List

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

from .model import Edge
from .schema import EdgeSchemaConvertingPos
from .service import EdgeService

api = Namespace("Edge", description="Single namespace, single entity")  # noqa


@api.route("/<string:graph_id>/<string:vertex>")
@api.route('/upload')
@api.param("graph_id", "Graph Id")
@api.param("vertex", "The vertex to query")
class Edges(Resource):

    @responds(schema=EdgeSchemaConvertingPos(many=True))
    def get(self, graph_id: int, vertex: str) -> List[Edge]:
        with SessionLocal() as db:
            edges = EdgeService.get_edges(vertex, graph_id, db)
            return edges
        
    def post(self):
     
        count = 0

        with SessionLocal() as db:
            for edge in iterate_stream(request):
                edge = edge.decode()
                edge = edge.split(",")
                
                v = Edge(
                    graph_id=edge[3].strip(),
                    src_id=edge[0].strip(),
                    trg_id=edge[1].strip(),
                    amount=edge[2].strip(),
                )
                db.add(v)
                count += 1
                
            db.commit()
            db.flush()

        print("Added", count, "edges")

        return Response(status=200)