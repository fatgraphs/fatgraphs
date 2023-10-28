from typing import List

from ..vertex_metadata.service import VertexMetadataService
from . import SearchTerm


class SearchTermService:

    @staticmethod
    def get_autocomplete_terms(graph_id, db) -> List[SearchTerm]:
        metadata = VertexMetadataService.get_all_by_graph_id(graph_id, db)
        types = {m.type for m in metadata}
        labels = {m.label for m in metadata}

        result = []

        result.extend([SearchTerm(type='type', value=e) for e in types])
        result.extend([SearchTerm(type='label', value=e) for e in labels])

        return result
