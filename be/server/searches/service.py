from typing import List

from . import SearchTerm
from .interface import SearchTermInterface
from ..vertex_metadata.service import VertexMetadataService


class SearchTermService:

    @staticmethod
    def get_recent_searches(db: object) -> List[SearchTerm]:
        return db.query(SearchTerm).all()

    @staticmethod
    def update_search_terms(metadata_object: SearchTermInterface, db: object):

        to_insert = SearchTerm(type=metadata_object['type'], value=metadata_object['value'])
        db.add(to_insert)
        db.commit()
        recent_metadata_searches = SearchTermService.get_recent_searches(db)
        if len(recent_metadata_searches) > 5:
            to_remove = recent_metadata_searches[0]
            db.delete(to_remove)

        db.commit()
        return SearchTermService.get_recent_searches(db)

    @staticmethod
    def get_autocomplete_terms(page, db):
        types = VertexMetadataService.get_unique_types(page, db)
        labels = VertexMetadataService.get_unique_labels(page, db)
        types = list(map(lambda e: SearchTerm(type='type', value=e), types))
        labels = list(map(lambda e: SearchTerm(type='label', value=e), labels))
        types.extend(labels)
        return types
