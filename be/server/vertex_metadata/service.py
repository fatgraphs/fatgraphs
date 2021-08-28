from typing import List

from .interface import VertexMetadataInterface
from .model import VertexMetadata
from ..graph.service import GraphService
from ..searches import AUTOCOMPLETE_TERMS_PER_PAGE


class VertexMetadataService:

    @staticmethod
    def get_by_eth(eth: str, db: object) -> List[VertexMetadata]:
        metadatas = db.query(VertexMetadata).filter_by(eth=eth).all()
        return metadatas

    @staticmethod
    def get_by_label(label: str,  db: object) -> List[VertexMetadata]:
        matches = db.query(VertexMetadata).filter_by(label=label).all()
        return matches

    @staticmethod
    def get_by_type(type: str, db: object) -> List[VertexMetadata]:
        matches = db.query(VertexMetadata).filter_by(type=type).all()
        return matches

    @staticmethod
    def create(metadata_to_insert: VertexMetadataInterface, db: object):

        new_metadata = VertexMetadata(
            eth=metadata_to_insert['eth'],
            type=metadata_to_insert['type'],
            label=metadata_to_insert['label'],
            description=metadata_to_insert['description'])

        db.add(new_metadata)
        db.commit()
        return new_metadata

    @staticmethod
    def get_unique_types(page, db) -> List[str]:
        return VertexMetadataService._get_unique_by(db, page, VertexMetadata.type)

    @staticmethod
    def get_unique_labels(page, db) -> List[str]:
        return VertexMetadataService._get_unique_by(db, page, VertexMetadata.label)

    @staticmethod
    def _get_unique_by(db, page, by):
        unique_terms = db.query(by) \
            .distinct(by) \
            .offset((page - 1) * AUTOCOMPLETE_TERMS_PER_PAGE) \
            .limit(AUTOCOMPLETE_TERMS_PER_PAGE).all()
        return list(map(lambda e: str(e[0]), unique_terms))

    @staticmethod
    def merge_with_account_type(db, graph_id: int):
        table_name = GraphService.get_vertex_table_name(graph_id)
        # VertexMetadata.
