from typing import List

from flask_accepts import responds
from flask_restx import Namespace, Resource

from be.server.gallery_categories import GalleryCategorySchema, GalleryCategory
from be.server.gallery_categories.service import GalleryCategoryService
from be.server.server import SessionLocal

api = Namespace("GalleryCategory", description="Each graph belongs to a category.")

@api.route("/")
class GalleryCategoryResource(Resource):

    @responds(schema=GalleryCategorySchema(many=True))
    def get(self) -> List[GalleryCategory]:
        with SessionLocal() as db:
            return GalleryCategoryService.get_all(db)