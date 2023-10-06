import random
import warnings
from typing import List

from psycopg2._psycopg import AsIs
from sqlalchemy import select
from sqlalchemy.sql import text

from be.configuration import (
    CONFIGURATIONS,
    EDGE_GLOBAL_TABLE,
)
from be.server import configs
from be.server.vertex.model import Vertex

from ..vertex.service import VertexService
from . import Edge

from sqlalchemy.orm import (
    joinedload,
)

warnings.simplefilter(action='ignore', category=UserWarning)


class EdgeService:

    in_out_map = {
            'in':Edge.trg_id, 
            'out':Edge.src_id
        }

    @staticmethod
    def ensure_edge_table_exists(table_name: str, graph_id: int, db):

        query = text(
            """
            CREATE TABLE IF NOT EXISTS :table_name
            PARTITION OF :edge_table 
            FOR VALUES IN :graph_id;
            """
        )

        index_creation = text(
            """
            CREATE INDEX IF NOT EXISTS :index_name ON :table_name (src_id, trg_id);
            """
        )
        
        with db.get_bind().connect() as conn:
            trans = conn.begin()

            conn.execute(
                query, 
                {
                    'table_name': AsIs(table_name),
                    'edge_table': AsIs(EDGE_GLOBAL_TABLE),
                    'graph_id': tuple([str(graph_id)]),
                }
            )
            
            conn.execute(
                index_creation, 
                {
                    'index_name': AsIs(table_name + '_src_index'),
                    'table_name': AsIs(table_name),
                }
            )

            trans.commit()


    @staticmethod
    def get_edges(vertex, graph_id, db) -> List[Edge]:

        # TODO no need to fetch the  vertex from DB maybe?
        vertex_object = VertexService.get_by_eths(graph_id, [vertex], db)[0]

        result = []
        result_in = EdgeService.get_edges_with_probability('in', vertex_object, graph_id, db)
        result_out = EdgeService.get_edges_with_probability('out', vertex_object, graph_id, db)

        half_edge_count = CONFIGURATIONS['endpoints']['parameters']['edges_fetched_limit'] // 2

        result.extend(
            random.sample(result_in,
                      min(half_edge_count, len(result_in))
            )
        )

        result.extend(
            random.sample(
                result_out,
                min(half_edge_count*2 - len(result), len(result_out))
            )
        )

        return result
    
    @staticmethod
    def get_edges_with_probability(in_out, vertex: Vertex, graph_id, ses) -> List[Edge]:
        limit = CONFIGURATIONS['endpoints']['parameters']['edges_fetched_limit']

        edge_count = (
            ses.query(Edge)
            .filter(EdgeService.in_out_map[in_out] == vertex.vertex)
            .count()
        )

        fetch_edges_query = (
            select(Edge)
            .options(joinedload(Edge.src))
            .options(joinedload(Edge.trg))
            .where(EdgeService.in_out_map[in_out] == vertex.vertex)
            .where(Edge.graph_id == graph_id)
        )

        if edge_count > limit:
            fetch_edges_query = (
                fetch_edges_query
                .limit(limit)
                .offset(random.randint(0, edge_count-limit))
            )

        res = ses.execute(fetch_edges_query)
        res = res.fetchall()
        return [e[0] for e in res]
