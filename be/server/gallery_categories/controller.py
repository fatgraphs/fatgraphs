from typing import List

from flask_accepts import responds
from flask_restx import Namespace, Resource

from . import GalleryCategorySchema, GalleryCategory
from .service import GalleryCategoryService
from .. import SessionLocal

api = Namespace("GalleryCategory", description="Each graph belongs to a category.")

@api.route("/")
class GalleryCategoryResource(Resource):

    @responds(schema=GalleryCategorySchema(many=True))
    def get(self) -> List[GalleryCategory]:
        with SessionLocal() as db:
            return GalleryCategoryService.get_all(db)