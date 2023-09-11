from typing import List

from geoalchemy2 import Geometry
from psycopg2._psycopg import AsIs
from sqlalchemy import Column
from sqlalchemy import Integer, String, Float, ForeignKey

from .. import Base, engine
from ..utils import to_pd_frame, wkt_to_x_y_list
from ...configuration import VERTEX_GLOBAL_TABLE, VERTEX_TABLE_NAME
from sqlalchemy.sql import text

class Vertex(Base):

    __tablename__ = "tg_vertex"

    graph_id = Column(Integer(), ForeignKey('tg_graphs.id'))
    vertex = Column(String(), primary_key=True)
    size = Column(Float(precision=8))
    pos = Column(Geometry('Point', 3857))

    @staticmethod
    def get_closest(graph_id: int, x: float, y: float):
        query = text(
            """
            SELECT graph_id, vertex, size, ST_AsText(ST_PointFromWKB(pos)), pos <-> ST_SetSRID(ST_MakePoint(:x, :y), 3857) AS dist 
            FROM :table_name 
            WHERE graph_id = :graph_id
            ORDER BY dist LIMIT 1;
            """
        )

        with engine.connect() as conn:
            result = conn.execute(
                query, 
                {
                    'table_name': AsIs(VERTEX_TABLE_NAME(graph_id)),
                    'graph_id': graph_id,
                    'x': x,
                    'y': y
                }
            )
            print({
                    'table_name': AsIs(VERTEX_TABLE_NAME(graph_id)),
                    'graph_id': graph_id,
                    'x': x,
                    'y': y
                })
            closest = to_pd_frame(result)
            print(result)

            for row in result:
                print(row)

            v = Vertex(graph_id=closest['graph_id'][0],
                    pos=wkt_to_x_y_list(closest['st_astext'][0]),
                    vertex=closest['vertex'][0],
                    size=closest['size'][0])
            return v

    @staticmethod
    def get(vertices: List[str], graph_id: int, db: object):

        query = text(
            """
            SELECT graph_id, vertex, size, ST_AsText(ST_PointFromWKB(pos)) AS pos 
            FROM :table_name 
            WHERE vertex IN :vertices
            """ 
        )

        substitution = {
            'table_name': AsIs(VERTEX_TABLE_NAME(graph_id)),
            'vertices': tuple(vertices)
        }

        with engine.connect() as conn:

            raw_result = conn.execute(query, substitution)
            print("raw_result", raw_result)

            fetchall = to_pd_frame(raw_result)

            return Vertex._map_to_model(fetchall)

    @staticmethod
    def _map_to_model(fetchall):
        collect = []
        for (i, e) in fetchall.iterrows():
            pos_as_list = wkt_to_x_y_list(e['pos'])
            vertex = Vertex(graph_id=e['graph_id'], vertex=e['vertex'], size=e['size'], pos=pos_as_list)
            collect.append(vertex)
        return collect
