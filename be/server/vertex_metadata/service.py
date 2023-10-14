from typing import List

import numpy as np
import pandas as pd
from psycopg2._psycopg import AsIs
from sqlalchemy import select
from sqlalchemy.sql import text

from be.server import configs

from .. import engine
from ..utils import to_pd_frame
from .interface import VertexMetadataInterface
from .model import VertexMetadata


class VertexMetadataService:

    @staticmethod
    def get_all_by_graph(graph_id: int, db) -> List[VertexMetadata]:
        vertex_metadatas = VertexMetadataService.merge_graph_vertices_with_metadata(graph_id, db)
        return vertex_metadatas[['vertex', 'account_type', 'type', 'label', 'icon']]

    @staticmethod
    def get_by_vertex(vertex: str, db) -> List[VertexMetadata]:
        query = select(VertexMetadata).filter(VertexMetadata.vertex == vertex)
        result = db.execute(query)
        return [e[0] for e in result.fetchall()]

    @staticmethod
    def get_by_label(label: str, db) -> List[VertexMetadata]:
        query = select(VertexMetadata).filter(VertexMetadata.label == label)
        result = db.execute(query)
        return [e[0] for e in result.fetchall()]
    
    @staticmethod
    def get_by_type(type: str, db) -> List[VertexMetadata]:
        query = select(VertexMetadata).filter(VertexMetadata.type == type)
        result = db.execute(query)
        return [e[0] for e in result.fetchall()]

    @staticmethod
    def create(metadata_to_insert: VertexMetadataInterface, db: object):

        new_metadata = VertexMetadata(
            vertex=metadata_to_insert['vertex'],
            type=metadata_to_insert['type'],
            label=metadata_to_insert['label'],
            account_type=metadata_to_insert.get('account_type'),
            description=metadata_to_insert['description'])

        created = db.add(new_metadata)
        db.commit()
        db.flush()
        return created

    @staticmethod
    def merge_graph_vertices_with_account_type(graph_id: int, db):
        table_name = configs.VERTEX_TABLE_NAME(graph_id)
        query = text(
            """
            SELECT tg_vertex_metadata.vertex, tg_vertex_metadata.account_type FROM :table_name
            INNER JOIN tg_vertex_metadata
            ON (tg_vertex_metadata.vertex = :table_name.vertex);
            """
        )        
        with engine.connect() as conn:
        
            execute = conn.execute(query, {'table_name': AsIs(table_name)})
            result = to_pd_frame(execute)
            result = result.fillna(0)
            result['account_type'] = result['account_type'].astype(np.int64)
            return result


    @staticmethod
    def merge_graph_vertices_with_metadata(graph_id, conn):
        table_name = configs.VERTEX_TABLE_NAME(graph_id)
        query = text(
            """
            SELECT * FROM :table_name
            INNER JOIN tg_vertex_metadata
            ON (tg_vertex_metadata.vertex = :table_name.vertex);
            """
        )
        
        execute = conn.execute(
            query, 
            {'table_name': AsIs(table_name)}
        )
        result = to_pd_frame(execute)
        if(len(list(result)) == 0): # if the result contains no columns (and no rows), manually add them
            result["vertex"] = None
            result["type"] = None
            result["label"] = None
            result["icon"] = None
        result = result.loc[:, ~result.columns.duplicated()]
        return result
