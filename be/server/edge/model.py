from typing import List
from geoalchemy2 import Geometry

from graph_tool import Edge
from psycopg2._psycopg import AsIs
from sqlalchemy.sql import text

from .. import engine
from ..utils import (
    to_pd_frame,
    wkt_to_x_y_list,
)
from ..vertex import Vertex

from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
)


class Edge:
    # = Column(Integer(), ForeignKey('tg_graphs.id'))

    table_name = "tg_edge"

    def __init__(self, graph_id: int, src: Vertex, trg: Vertex, amount: float):
        self.graph_id = graph_id
        self.src = src
        self.trg = trg
        self.amount = amount

    def add(self, db):
        query = text(
            """
            INSERT INTO :edge_table_name
            (graph_id, src, trg, amount) 
            VALUES (
                :graph_id,
                :src_vertex,
                :trg_vertex,
                :amount);
            """
        )
        
        result = db.execute(
            query, 
            {
                'edge_table_name': AsIs(Edge.table_name),
                'graph_id': self.graph_id,
                'src_vertex': self.src.vertex,
                'trg_vertex': self.trg.vertex,
                'amount': self.amount
            }
        )



    @staticmethod
    def get_edges(graph_id, vertex, prob) -> List[Edge]:
        query = text(
            """
            SELECT * FROM tg_edge 
            WHERE ((src = :query_src OR trg = :query_src) 
            AND (graph_id = :graph_id)) AND random() < :prob;
            """
        )
        with engine.connect() as conn:
            query_result = conn.execute(query, {
                'graph_id': graph_id,
                'query_src': vertex,
                'prob': AsIs(prob)
                }
            )

            frame = to_pd_frame(query_result)

            return Edge._map_to_model(frame)


    @staticmethod
    def get_out_edges_with_probability(edge_table, vertex_table, vertex: Vertex, prob, graph_id) -> List[Edge]:
        query = text(
            """
            SELECT :edge_table.src, :edge_table.trg, :edge_table.amount,
            vertextarget.size as trg_size, 
            ST_AsText(ST_PointFromWKB(vertextarget.pos)) as pos_trg
            FROM :edge_table
            LEFT JOIN :vertex_table vertextarget ON :edge_table.trg = vertextarget.vertex 
            WHERE :edge_table.src = :vertex
            AND random() < :prob;
            """
        )

        with engine.connect() as conn:

            query_result = conn.execute(query, {
                'edge_table': AsIs(edge_table),
                'vertex_table': AsIs(vertex_table),
                'vertex': vertex.vertex,
                'prob': AsIs(prob)
            }
                                        )
            frame = to_pd_frame(query_result)

            return Edge._map_to_model_trg_only(frame, vertex, graph_id)

    @staticmethod
    def get_in_edges_with_probability(edge_table, vertex_table, vertex: Vertex, prob, graph_id) -> List[Edge]:
        query = text(
            """
            SELECT :edge_table.src, :edge_table.trg, :edge_table.amount,
                vertexsource.size as src_size,
                ST_AsText(ST_PointFromWKB(vertexsource.pos)) as pos_src
            FROM :edge_table
            LEFT JOIN :vertex_table vertexsource ON :edge_table.src = vertexsource.vertex
            WHERE :edge_table.trg = :vertex 
            AND random() < :prob;
            """
        )

        with engine.connect() as conn:

            query_result = conn.execute(
                query, 
                {
                    'edge_table': AsIs(edge_table),
                    'vertex_table': AsIs(vertex_table),
                    'vertex': vertex.vertex,
                    'prob': AsIs(prob)
                }
            )
            frame = to_pd_frame(query_result)

            return Edge._map_to_model_src_only(frame, vertex, graph_id)

    @staticmethod
    def get_count(edge_table, vertex, inout='both'):
        query = text(
            """
            SELECT count(*) FROM :edge_table 
            WHERE src = :vertex OR trg = :vertex;
            """
        )
        if inout == 'in':
            query = text(
                """
                SELECT count(*) FROM :edge_table 
                WHERE trg = :vertex;
                """
            )
        if inout == 'out':
            query = text(
                """
                SELECT count(*) FROM :edge_table 
                WHERE src = :vertex;
                """
            )
        with engine.connect() as conn:
            query_result = conn.execute(
                query, 
                {
                    'vertex': vertex,
                    'edge_table': AsIs(edge_table)
                }
            )
            return query_result.fetchall()[0][0]

    @staticmethod
    def _map_to_model_trg_only(frame, src_vertex, graph_id):
        collect = []
        for (i, e) in frame.iterrows():
            pos_trg = wkt_to_x_y_list(e['pos_trg'])
            trg_vertex = Vertex(graph_id=graph_id, vertex=e['trg'], size=e['trg_size'], pos=pos_trg)
            edge = Edge(
                graph_id=graph_id,
                src=src_vertex,
                trg=trg_vertex,
                amount=e['amount'],
            )
            collect.append(edge)
        return collect

    @staticmethod
    def _map_to_model_src_only(frame, trg_vertex, graph_id):
        collect = []
        for (i, e) in frame.iterrows():
            pos_src = wkt_to_x_y_list(e['pos_src'])
            src_vertex = Vertex(graph_id=graph_id, vertex=e['src'], size=e['src_size'], pos=pos_src)
            edge = Edge(
                graph_id=graph_id,
                src=src_vertex,
                trg=trg_vertex,
                amount=e['amount'],
            )
            collect.append(edge)
        return collect
