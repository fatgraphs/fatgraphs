from typing import List
from psycopg2._psycopg import AsIs

from .interface import VertexMetadataInterface
from .model import VertexMetadata
from .. import engine
from ..graph.service import GraphService
from ..searches import AUTOCOMPLETE_TERMS_PER_PAGE
from ..utils import to_pd_frame


class VertexMetadataService:

    @staticmethod
    def get_by_eth(eth: str, db) -> List[VertexMetadata]:
        result = VertexMetadata.filter_by(db, eth=eth )
        return result

    @staticmethod
    def get_by_label(label: str, db) -> List[VertexMetadata]:
        result = VertexMetadata.filter_by(db, label=label)
        return result

    @staticmethod
    def get_by_type(type: str, db) -> List[VertexMetadata]:
        result = VertexMetadata.filter_by(db, type=type)
        return result

    @staticmethod
    def create(metadata_to_insert: VertexMetadataInterface, db: object):

        new_metadata = VertexMetadata(
            eth=metadata_to_insert['eth'],
            type=metadata_to_insert['type'],
            label=metadata_to_insert['label'],
            account_type=metadata_to_insert['account_type'],
            description=metadata_to_insert['description'])

        # db.add(new_metadata)
        new_metadata.add(db)
        db.commit()
        return new_metadata

    @staticmethod
    def get_unique_types(page, db) -> List[str]:
        return VertexMetadata.get_unique_by(db, page, 'type')

    @staticmethod
    def get_unique_labels(page, db) -> List[str]:
        return VertexMetadata.get_unique_by(db, page, 'label')


    @staticmethod
    def merge_with_account_type(db, graph_id: int):
        table_name = GraphService.get_vertex_table_name(graph_id, db)
        query = """SELECT vertex, type FROM %(table_name)s
                    INNER JOIN tg_account_type
                    ON (tg_account_type.vertex = %(table_name)s.eth);"""
        execute = db.bind.engine.execute(query, {'table_name': AsIs(table_name)})
        frame = to_pd_frame(execute)
        return frame


    @staticmethod
    def merge_with_types(db, graph_id):
        table_name = GraphService.get_vertex_table_name(graph_id, db)
        query = """SELECT eth, icon FROM %(table_name)s
                    INNER JOIN tg_vertex_metadata
                    ON (tg_vertex_metadata.eth = %(table_name)s.eth);"""
        execute = db.bind.engine.execute(query, {'table_name': AsIs(table_name)})
        result = to_pd_frame(execute)
        # result = frame[frame.icon.notnull()]
        result = result.loc[: , ~result.columns.duplicated()]
        return result
