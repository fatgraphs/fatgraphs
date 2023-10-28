from typing import List

import numpy as np
import pandas as pd
from psycopg2._psycopg import AsIs
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import text

from be.server import configs
from be.server.vertex.model import Vertex

from .. import engine
from ..utils import to_pd_frame
from .interface import VertexMetadataInterface
from .model import VertexMetadata


class VertexMetadataService:

    @staticmethod
    def get_all_by_graph(graph_id: int, db) -> List[VertexMetadata]:
        vertex_metadatas = VertexMetadataService.get_all_by_graph_id(graph_id, db)
        return vertex_metadatas

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
    def get_all_by_graph_id(graph_id, conn):
        vertices_query = select(Vertex.vertex).filter(Vertex.graph_id == graph_id)
        vertices = conn.execute(vertices_query)
        vertices = vertices.fetchall()
        vertices = [e[0] for e in vertices]

        fetch_edges_query = (
            select(VertexMetadata)
            .where(Vertex.vertex.in_(vertices))
        )

        res = conn.execute(fetch_edges_query)
        res = res.fetchall()
        return [e[0] for e in res]
