from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from flask.wrappers import Response
from typing import List

from .schema import UserSchema
from .service import UserService
from .model import User
from .interface import UserInterface

api = Namespace("User", description="Single namespace, single entity")  # noqa


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


@api.route("/<string:user_name>")
@api.param("user_name", "User Name")
class UserNameResource(Resource):
    @responds(schema=UserSchema)
    def get(self, user_name: str) -> User:
        return UserService.get_by_name(user_name)


@api.route("/search-term/<string:user_name>/<string:search_term>")
@api.param("user_name", "User Name")
@api.param("search_term", "The new search term to add")
class SearchTermResource(Resource):

    @responds(schema=UserSchema)
    def put(self, user_name: str, search_term: str) -> UserSchema:
        return UserService.update_search_terms(user_name, search_term)

    # def delete(self, widgetId: int) -> Response:
    #     """Delete Single Widget"""
    #     from flask import jsonify
    #
    #     id = GraphService.delete_by_id(widgetId)
    #     return jsonify(dict(status="Success", id=id))
    #
    # @accepts(schema=GraphSchema, api=api)
    # @responds(schema=GraphSchema)
    # def put(self, widgetId: int) -> Graph:
    #     """Update Single Widget"""
    #
    #     changes: GraphInterface = request.parsed_obj
    #     Widget = GraphService.get_by_id(widgetId)
    #     return GraphService.update(Widget, changes)
