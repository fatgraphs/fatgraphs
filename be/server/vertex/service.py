from typing import List
import pandas as pd
from geoalchemy2 import Geometry, WKTElement
import geopandas as gpd
from psycopg2._psycopg import AsIs

from be.configuration import SRID, VERTEX_TABLE_NAME, VERTEX_GLOBAL_TABLE
from .model import Vertex
from .. import engine
from ..graph.service import GraphService
from ..vertex_metadata.service import VertexMetadataService

import warnings

warnings.simplefilter(action='ignore', category=UserWarning)


class VertexService:

    @staticmethod
    def get_closest(graph_id: int, x: float, y: float, db) -> Vertex:
        closest = Vertex.get_closest(graph_id, x, y, db)
        return closest

    @staticmethod
    def get_by_eths(graph_id: int, eths: List[str], db) -> List[Vertex]:
        if len(eths) == 0:
            return []
        vertices = Vertex.get(eths, graph_id, db)
        return vertices

    @staticmethod
    def ensure_vertex_table_exists(table_name: str, graph_id: int):

        query = """CREATE TABLE IF NOT EXISTS %(table_name)s 
        PARTITION OF %(vertex_table)s 
        FOR VALUES IN %(graph_id)s;"""
        engine.execute(query, {'table_name': AsIs(table_name),
                               'vertex_table': AsIs(VERTEX_GLOBAL_TABLE),
                               'graph_id': tuple([str(graph_id)])})

    @staticmethod
    def attach_metadata(vertices, db):
        if not isinstance(vertices, list):
            vertices = [vertices]
        for v in vertices:
            metadata = VertexMetadataService.get_by_eth(v.vertex, db)
            for m in metadata:
                for attr in ['types', 'labels']:
                    existing = getattr(v, attr, [])
                    existing.append(getattr(m, attr[0:-1]))
                    setattr(v, attr, existing)
        return vertices

    @staticmethod
    def get_by_type(graph_id, type, db):
        global_matches = VertexMetadataService.get_by_type(type, db)
        if graph_id is not None:
            global_eths = list(map(lambda e: e.vertex, global_matches))
            this_graph_matches = VertexService.get_by_eths(graph_id, global_eths, db)
            return this_graph_matches
        return global_matches

    @staticmethod
    def get_by_label(graph_id, label, db):
        global_matches = VertexMetadataService.get_by_label(label, db)
        if graph_id is not None:
            global_eths = list(map(lambda e: e.vertex, global_matches))
            this_graph_matches = VertexService.get_by_eths(graph_id, global_eths, db)
            return this_graph_matches
        return global_matches

    @staticmethod
    def get_by_eth_across_graphs(eth, db):
        return Vertex.get([eth], None, db)

