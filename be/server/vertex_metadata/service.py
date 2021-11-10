from typing import List
from psycopg2._psycopg import AsIs

from .interface import VertexMetadataInterface
from .model import VertexMetadata
from ..graph.service import GraphService
from ..utils import to_pd_frame
import numpy as np

from ...configuration import VERTEX_TABLE_NAME


class VertexMetadataService:

    @staticmethod
    def get_by_eth(vertex: str, db) -> List[VertexMetadata]:
        result = VertexMetadata.filter_by(db, vertex=vertex )
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
            vertex=metadata_to_insert['vertex'],
            type=metadata_to_insert['type'],
            label=metadata_to_insert['label'],
            account_type=metadata_to_insert.get('account_type'),
            description=metadata_to_insert['description'])

        # db.add(new_metadata)
        new_metadata.add(db)
        db.commit()
        return new_metadata

    @staticmethod
    def delete(vertex, typee, value, db):
        return VertexMetadata.delete(vertex, typee, value, db)

    @staticmethod
    def merge_graph_vertices_with_account_type(db, graph_id: int):
        table_name = VERTEX_TABLE_NAME(graph_id)
        query = """SELECT tg_account_type.vertex, tg_account_type.type FROM %(table_name)s
                    INNER JOIN tg_account_type
                    ON (tg_account_type.vertex = %(table_name)s.vertex);"""
        execute = db.bind.engine.execute(query, {'table_name': AsIs(table_name)})
        result = to_pd_frame(execute)
        result['type'] = result['type'].astype(np.int64)
        return result


    @staticmethod
    def merge_graph_vertices_with_metadata(graph_id, db):
        table_name = VERTEX_TABLE_NAME(graph_id)
        query = """SELECT * FROM %(table_name)s
                    INNER JOIN tg_vertex_metadata
                    ON (tg_vertex_metadata.vertex = %(table_name)s.vertex);"""
        execute = db.bind.engine.execute(query, {'table_name': AsIs(table_name)})
        result = to_pd_frame(execute)
        result = result.loc[:, ~result.columns.duplicated()]
        return result
