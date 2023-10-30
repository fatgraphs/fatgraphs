import random
import warnings
from typing import List

from psycopg2._psycopg import AsIs
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import text


from be.server.edge import Edge
from be.server.server import app


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
                    'edge_table': AsIs(app.config['EDGE_GLOBAL_TABLE']),
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
    def get_edges(vertex_ext_id, graph_id, db) -> List[Edge]:

        result = []
        result_in = EdgeService.get_edges_with_probability('in', vertex_ext_id, graph_id, db)
        result_out = EdgeService.get_edges_with_probability('out', vertex_ext_id, graph_id, db)

        half_edge_count = app.config['MAX_EDGES_DISPLAY'] // 2

        count_in = min(half_edge_count, len(result_in))

        result.extend(
            random.sample(
                result_in,
                count_in
            )
        )

        result.extend(
            random.sample(
                result_out,
                min(half_edge_count*2 - count_in, len(result_out))
            )
        )

        return result
    
    @staticmethod
    def get_edges_with_probability(in_out, vertex_ext_id: str, graph_id, ses) -> List[Edge]:
        limit = app.config['MAX_EDGES_DISPLAY']

        edge_count = EdgeService.get_edge_count(in_out, vertex_ext_id, graph_id,ses)

        fetch_edges_query = (
            select(Edge)
            .options(joinedload(Edge.src))
            .options(joinedload(Edge.trg))
            .where(EdgeService.in_out_map[in_out] == vertex_ext_id)
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
    
    @staticmethod
    def get_edge_count(in_out, vertex_ext_id: str, graph_id: int, ses) -> int:
        return (
            ses.query(Edge)
            .filter(EdgeService.in_out_map[in_out] == vertex_ext_id)
            .filter(Edge.graph_id == graph_id)
            .count()
        )
