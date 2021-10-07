from typing import List
from psycopg2._psycopg import AsIs
from be.configuration import EDGE_GLOBAL_TABLE, CONFIGURATIONS
from . import Edge
from .. import engine

import warnings
from ..graph.service import GraphService
from ..utils import to_pd_frame

warnings.simplefilter(action='ignore', category=UserWarning)


class EdgeService:

    @staticmethod
    def ensure_edge_table_exists(table_name: str, graph_id: int):

        query = """CREATE TABLE IF NOT EXISTS %(table_name)s 
        PARTITION OF %(edge_table)s 
        FOR VALUES IN %(graph_id)s;"""
        engine.execute(query, {'table_name': AsIs(table_name),
                               'edge_table': AsIs(EDGE_GLOBAL_TABLE),
                               'graph_id': tuple([str(graph_id)])})
        index_creation = """
            CREATE INDEX IF NOT EXISTS %(index_name)s ON %(table_name)s (src, trg);"""
        engine.execute(index_creation, {
            'index_name': AsIs(table_name + '_src_index'),
            'table_name': AsIs(table_name)})


    @staticmethod
    def ensure_index_edge_table(edge_table, graph_id):
        pass

    @staticmethod
    def get_edge_count(edge_table, vertex):
        result = Edge.get_count(edge_table, vertex)
        return result


    @staticmethod
    def get_edges(vertex, graph_id, db) -> List[Edge]:

        def probability_choosing_edge():
                count = EdgeService.get_edge_count(edge_table, vertex)
                prob = 1.0 if count < CONFIGURATIONS['endpoints']['parameters']['edges_fetched_limit'] \
                            else CONFIGURATIONS['endpoints']['parameters']['edges_fetched_limit']/count
                return prob

        edge_table = GraphService.get_edge_table_name(graph_id, db)
        vertex_table = GraphService.get_vertex_table_name(graph_id, db)
        prob = probability_choosing_edge()
        result = Edge.get_edges_with_probability(edge_table, vertex_table, vertex, prob, graph_id)
        return result

