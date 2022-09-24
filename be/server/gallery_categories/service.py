from typing import List

from be.server.gallery_categories import GalleryCategory


class GalleryCategoryService:

    @staticmethod
    def get_all(db) -> List[GalleryCategory]:
        graphs = db.query(GalleryCategory).all()
        return graphs