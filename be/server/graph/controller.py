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

api = Namespace("Graph", description="Single namespace, single entity")  # noqa


@api.route("/create")
class GraphResource(Resource):

    @accepts(schema=GraphSchema, api=api)
    @responds(schema=GraphSchema)
    def post(self) -> Graph:
        with SessionLocal() as db:
            return GraphService.create(request.parsed_obj, db)

@api.route("/byuser/<string:user_name>")
@api.param("user_name", "User Name")
class GraphUserNameResource(Resource):

    @responds(schema=GraphSchema(many=True))
    def get(self, user_name: str) -> List[Graph]:
        with SessionLocal() as db:
            return GraphService.get_by_owner(user_name, db)


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
