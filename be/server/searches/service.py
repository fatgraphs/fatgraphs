from typing import List

from . import SearchTerm
from .interface import SearchTermInterface
from ..vertex_metadata.service import VertexMetadataService


class SearchTermService:

    @staticmethod
    def get_autocomplete_terms(page, db) -> List[SearchTerm]:
        types = VertexMetadataService.get_unique_types(page, db)
        labels = VertexMetadataService.get_unique_labels(page, db)
        types = list(map(lambda e: SearchTerm(type='type', value=e), types))
        labels = list(map(lambda e: SearchTerm(type='label', value=e), labels))
        types.extend(labels)
        return types
