from typing import List
from flask import request
from flask_accepts import responds, accepts
from flask_restx import Namespace, Resource
from .model import Edge
from .schema import EdgeSchema
from .service import EdgeService
from .. import SessionLocal

import random
from ..graph.service import GraphService
from ...configuration import CONFIGURATIONS

api = Namespace("Edge", description="Single namespace, single entity")  # noqa


@api.route("/<string:graph_id>/<string:vertex>")
@api.param("graph_id", "Graph Id")
@api.param("vertex", "The vertex to query")
class GetEdges(Resource):

    @responds(schema=EdgeSchema(many=True))
    def get(self, graph_id: int, vertex: str) -> List[Edge]:
        with SessionLocal() as db:
            edges = EdgeService.get_edges(vertex, graph_id, db)
            edges_100 = random.sample(edges,
                    min(CONFIGURATIONS['endpoints']['parameters']['edges_fetched_limit'], len(edges)))
            return edges_100

