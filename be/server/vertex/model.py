from typing import List
from geoalchemy2 import Geometry
from psycopg2._psycopg import AsIs
from sqlalchemy import Integer, Column, String, Float, ForeignKey
from .. import Base, engine
from ..utils import to_pd_frame, wkt_to_x_y_list
from sqlalchemy import  Column


class Vertex(Base):

    __tablename__ = "tg_vertex"

    graph_id = Column(Integer(), ForeignKey('tg_graphs.id'))
    eth = Column(String(), primary_key=True)
    size = Column(Float(precision=8))
    pos = Column(Geometry('Point', 3857))


    @staticmethod
    def get_closest(graph_id: int, x: float, y: float, db):
        query = """SELECT graph_id, eth, size, ST_AsText(ST_PointFromWKB(pos)), pos <-> ST_SetSRID(ST_MakePoint(%(x)s, %(y)s), 3857) AS dist 
                FROM %(table_name)s 
                WHERE graph_id = %(graph_id)s
                ORDER BY dist LIMIT 1;
                """

        result = engine.execute(query, {
            'table_name': AsIs(Vertex.__tablename__),
            'graph_id': graph_id,
            'x': x,
            'y': y
        })
        closest = to_pd_frame(result)
        v = Vertex(graph_id=closest['graph_id'][0],
                   pos=wkt_to_x_y_list(closest['st_astext'][0]),
                   eth=closest['eth'][0],
                   size=closest['size'][0])
        return v

    @staticmethod
    def get_in_list(eths: List[str], table_name: str, db: object):
        query = """SELECT graph_id, eth, size, ST_AsText(ST_PointFromWKB(pos)) AS pos FROM %(table_name)s WHERE %(table_name)s.eth IN %(eths)s;
        """
        raw_result = engine.execute(query, {'table_name': AsIs(table_name),
                                         'eths': tuple(eths)})
        db.commit()
        fetchall = to_pd_frame(raw_result)

        return Vertex._map_to_model(fetchall)


    @staticmethod
    def get_by_eth_across_graphs(eth: str, db: object):
        query = """SELECT graph_id, eth, size, ST_AsText(ST_PointFromWKB(pos)) AS pos  
        FROM tg_vertex 
        WHERE eth = %(eth)s;"""
        raw_result = engine.execute(query, {'eth': eth})
        fetchall = to_pd_frame(raw_result)
        return Vertex._map_to_model(fetchall)

    @staticmethod
    def _map_to_model(fetchall):
        collect = []
        for (i, e) in fetchall.iterrows():
            pos_as_list = wkt_to_x_y_list(e['pos'])
            vertex = Vertex(graph_id=e['graph_id'], eth=e['eth'], size=e['size'], pos=pos_as_list)
            collect.append(vertex)
        return collect
