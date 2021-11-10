import random
from typing import List
from psycopg2._psycopg import AsIs
from be.configuration import EDGE_GLOBAL_TABLE, CONFIGURATIONS, VERTEX_TABLE_NAME, EDGE_TABLE_NAME
from . import Edge
from .. import engine

import warnings
from ..graph.service import GraphService
from ..utils import to_pd_frame
from ..vertex.service import VertexService

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
    def get_edge_count(edge_table, vertex, inout='both'):
        result = Edge.get_count(edge_table, vertex, inout)
        return result


    @staticmethod
    def get_edges(vertex, graph_id, db) -> List[Edge]:
        edge_table = EDGE_TABLE_NAME(graph_id)
        vertex_table = VERTEX_TABLE_NAME(graph_id)
        prob_in, prob_out = EdgeService._probabilities_choosing_edge(edge_table, vertex)
        vertex_object = VertexService.get_by_eths(graph_id, [vertex], db)[0]

        result = []
        result_in = Edge.get_in_edges_with_probability(edge_table, vertex_table, vertex_object, prob_in, graph_id)
        result_out = Edge.get_out_edges_with_probability(edge_table, vertex_table, vertex_object, prob_out, graph_id)

        half_edge_count = CONFIGURATIONS['endpoints']['parameters']['edges_fetched_limit'] // 2
        result.extend(
            random.sample(result_in,
                      min(half_edge_count, len(result_in))
            )
        )
        result.extend(
            random.sample(result_out,
                          min(half_edge_count*2 - len(result), len(result_out))
            )
        )

        return result

    @staticmethod
    def _probabilities_choosing_edge(edge_table, vertex):
        count_in = EdgeService.get_edge_count(edge_table, vertex, 'in')
        count_out = EdgeService.get_edge_count(edge_table, vertex, 'out')
        prob_in = 1.0 if count_in < CONFIGURATIONS['endpoints']['parameters']['edges_fetched_limit'] \
            else CONFIGURATIONS['endpoints']['parameters']['edges_fetched_limit'] / count_in
        prob_out = 1.0 if count_out < CONFIGURATIONS['endpoints']['parameters']['edges_fetched_limit'] \
            else CONFIGURATIONS['endpoints']['parameters']['edges_fetched_limit'] / count_out
        return prob_in, prob_out

