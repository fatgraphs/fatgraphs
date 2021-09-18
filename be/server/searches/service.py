from typing import List

from . import SearchTerm
from .interface import SearchTermInterface
from ..vertex_metadata.service import VertexMetadataService


class SearchTermService:

    @staticmethod
    def get_autocomplete_terms(graph_id, db) -> List[SearchTerm]:

        metadata = VertexMetadataService.merge_graph_vertices_with_metadata(db, graph_id)

        types = metadata.type.unique()
        labels = metadata.label.unique()

        result = []

        result.extend(list(map(lambda e: SearchTerm(type='type', value=e), types)))
        result.extend(list(map(lambda e: SearchTerm(type='label', value=e), labels)))

        return result
