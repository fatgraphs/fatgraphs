from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from flask.wrappers import Response
from typing import List
from . import GalleryCategorySchema, GalleryCategory
from .service import GalleryCategoryService


from .. import SessionLocal
from ..vertex.service import VertexService

api = Namespace("GalleryCategory", description="Each graph belongs to a category.")

@api.route("/")
class GalleryCategoryResource(Resource):

    @responds(schema=GalleryCategorySchema(many=True))
    def get(self) -> List[GalleryCategory]:
        with SessionLocal() as db:
            return GalleryCategoryService.get_all(db)