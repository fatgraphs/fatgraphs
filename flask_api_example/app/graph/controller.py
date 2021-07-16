from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from flask.wrappers import Response
from typing import List

from .schema import GraphSchema
from .service import GraphService
from .model import Graph

api = Namespace("Graph", description="Single namespace, single entity")  # noqa


# @api.route("/")
# class GraphResource(Resource):
#     """Widgets"""
#
#     @responds(schema=GraphSchema, many=True)
#     def get(self) -> List[Graph]:
#
#         return GraphService.get_all()
#
#     @accepts(schema=GraphSchema, api=api)
#     @responds(schema=GraphSchema)
#     def post(self) -> Graph:
#         """Create a Single Widget"""
#
#         return GraphService.create(request.parsed_obj)

@api.route("/create")
class GraphResource(Resource):

    @accepts(schema=GraphSchema, api=api)
    @responds(schema=GraphSchema)
    def post(self) -> Graph:
        return GraphService.create(request.parsed_obj)

@api.route("/byuser/<string:user_name>")
@api.param("user_name", "User Name")
class GraphUserNameResource(Resource):

    @responds(schema=GraphSchema(many=True))
    def get(self, user_name: str) -> List[Graph]:
        return GraphService.get_by_owner(user_name)


@api.route("/byname/<string:graph_name>")
@api.param("graph_name", "Graph Name")
class GraphNameResource(Resource):

    @responds(schema=GraphSchema)
    def get(self, graph_name: str) -> Graph:
        return GraphService.get_by_name(graph_name)
