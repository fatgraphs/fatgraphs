from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from .schema import UserSchema
from .service import UserService
from .model import User
from .. import SessionLocal
from ..metadata.schema import AutocompleteTermSchema
from ..metadata.service import MetadataService

api = Namespace("User", description="Single namespace, single entity")  # noqa


@api.route("/<string:user_name>")
@api.param("user_name", "User Name")
class UserNameResource(Resource):
    @responds(schema=UserSchema)
    def get(self, user_name: str) -> User:
        with SessionLocal() as db:
            return UserService.get_by_name(user_name, db)


@api.route("/search-term/<string:user_name>")
@api.param("user_name", "User Name")
class SearchTermResource(Resource):

    @responds(schema=AutocompleteTermSchema(many=True))
    def get(self, user_name: str) -> UserSchema:
        with SessionLocal() as db:
            user = UserService.get_by_name(user_name, db)
            objects = MetadataService.assemble_recent_searches(user)
            return objects


    @accepts(schema=AutocompleteTermSchema, api=api)
    @responds(schema=UserSchema)
    def put(self, user_name: str) -> UserSchema:
        with SessionLocal() as db:
            return UserService.update_search_terms(user_name, request.parsed_obj, db)