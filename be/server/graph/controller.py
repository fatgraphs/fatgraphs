from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from flask.wrappers import Response
from typing import List

from .interface import GraphInterface
from .schema import GraphSchema
from .service import GraphService
from .model import Graph
from .. import SessionLocal
from ..vertex.service import VertexService

api = Namespace("Graph", description="Graphs are saved with their metadata, but the actual vertices and edges are in the vertex and edge endpoints")

@api.route("/")
class GraphResource(Resource):

    @responds(schema=GraphSchema(many=True))
    def get(self) -> List[Graph]:
        with SessionLocal() as db:
            return GraphService.get_all(db)


@api.route("/<int:graph_id>")
@api.param("graph_id", "Graph Id")
class GraphIdResource(Resource):

    @responds(schema=GraphSchema)
    def get(self, graph_id: int) -> Graph:
        with SessionLocal() as db:
            return GraphService.get_by_id(graph_id, db)

    @accepts(schema=GraphSchema, api=api)
    @responds(schema=GraphSchema)
    def put(self, graph_id: int) -> Graph:
        with SessionLocal() as db:
            changes: GraphInterface = request.parsed_obj
            graph = GraphService.get_by_id(graph_id, db)
            return GraphService.update(graph, changes, db)


@api.route("/<string:eth>")
@api.param("eth", "Eth address searched across graphs")
class GraphByEthResource(Resource):

    @responds(schema=GraphSchema(many=True))
    def get(self, eth: str) -> List[Graph]:
        with SessionLocal() as db:
            vertices = VertexService.get_by_eth_across_graphs(eth, db)
            graph_ids = set(map(lambda vertex: vertex.graph_id, vertices))
            graphs = list(map(lambda id: GraphService.get_by_id(id, db), graph_ids))
            return graphs