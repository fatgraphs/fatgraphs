from typing import List

from geoalchemy2 import Geometry
from graph_tool import Edge
from psycopg2._psycopg import AsIs
from sqlalchemy import Column
from sqlalchemy import Integer, String, Float, ForeignKey

from .. import Base, engine
from ..utils import to_pd_frame, wkt_to_x_y_list
from ..vertex import Vertex
from ...configuration import VERTEX_GLOBAL_TABLE


class Edge:
    # = Column(Integer(), ForeignKey('tg_graphs.id'))

    table_name = "tg_edge"


    def __init__(self, graph_id: int, src: Vertex, trg: Vertex, amount: float, block_number: int):
        self.graph_id = graph_id
        self.src = src
        self.trg = trg
        self.block_number = block_number
        self.amount = amount

    def add(self, db):
       query = """INSERT INTO %(edge_table_name)s
       (graph_id, src_vertex, trg_vertex, block_number, amount) 
       VALUES (
           %(graph_id)s,
           %(src_vertex)s,
           %(trg_vertex)s,
           %(block_number)s,
           %(amount)s);"""

       result = db.bind.engine.execute(query, {
           'edge_table_name': AsIs(Edge.table_name),
           'graph_id': self.graph_id,
           'src_vertex': self.src.vertex,
           'trg_vertex': self.trg.vertex,
           'block_number': self.block_number,
           'amount': self.amount
       })



    @staticmethod
    def get_edges(graph_id, vertex, prob) -> List[Edge]:
        query = """SELECT * FROM tg_edge WHERE ((src = %(query_src)s OR trg = %(query_src)s) 
            AND (graph_id = %(graph_id)s)) AND random() < %(prob)s;
        """
        query_result = engine.execute(query, {
            'graph_id': graph_id,
            'query_src': vertex,
            'prob': AsIs(prob)
            }
        )
        frame = to_pd_frame(query_result)
        return Edge._map_to_model(frame)

    @staticmethod
    def get_edges_with_probability(edge_table, vertex_table, vertex, prob, graph_id) -> List[Edge]:

        query = """SELECT %(edge_table)s.src, %(edge_table)s.trg, %(edge_table)s.amount, %(edge_table)s.block_number, 
            vertexsource.size as src_size, vertextarget.size as trg_size, 
            ST_AsText(ST_PointFromWKB(vertexsource.pos)) as pos_src, 
            ST_AsText(ST_PointFromWKB(vertextarget.pos)) as pos_trg
        FROM %(edge_table)s
        LEFT JOIN %(vertex_table)s vertextarget ON  %(edge_table)s.trg = vertextarget.vertex 
		LEFT JOIN %(vertex_table)s vertexsource ON %(edge_table)s.src = vertexsource.vertex
        WHERE (%(edge_table)s.src = %(vertex)s OR %(edge_table)s.trg = %(vertex)s) 
        AND random() < %(prob)s;
        """

        query_result = engine.execute(query, {
            'edge_table': AsIs(edge_table),
            'vertex_table': AsIs(vertex_table),
            'vertex': vertex,
            'prob': AsIs(prob)
            }
        )
        frame = to_pd_frame(query_result)

        return Edge._map_to_model(frame, graph_id)

    @staticmethod
    def get_count(edge_table, vertex):
        query = """SELECT count(*) FROM %(edge_table)s 
            WHERE src = %(vertex)s OR trg = %(vertex)s;
        """
        query_result = engine.execute(query, {
            'vertex': vertex,
            'edge_table': AsIs(edge_table)
        })
        return query_result.fetchall()[0][0]


    @staticmethod
    def _map_to_model(frame, graph_id):
        collect = []
        for (i, e) in frame.iterrows():
            pos_trg = wkt_to_x_y_list(e['pos_trg'])
            pos_src = wkt_to_x_y_list(e['pos_src'])
            src_vertex = Vertex(graph_id=graph_id, vertex=e['src'], size=e['src_size'], pos=pos_src)
            trg_vertex = Vertex(graph_id=graph_id, vertex=e['trg'], size=e['trg_size'], pos=pos_trg)
            edge = Edge(
                graph_id=graph_id,
                src=src_vertex,
                trg=trg_vertex,
                amount=e['amount'],
                block_number=e['block_number']
            )
            collect.append(edge)
        return collect
