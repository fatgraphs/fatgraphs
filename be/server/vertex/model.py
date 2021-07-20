from typing import List
from geoalchemy2 import Geometry
from geopandas.array import from_wkb, from_wkt
from graph_tool import Vertex
from psycopg2._psycopg import AsIs
from sqlalchemy import Integer, Column, String, Float, ForeignKey
from sqlalchemy.orm import mapper

from .interface import VertexInterface
from .. import Base, engine
from ..utils import to_pd_frame, wkt_to_x_y_list
from sqlalchemy import MetaData, Table, Column


def getDynamicVertexModel(name):
    metadata = Base.metadata
    if name in metadata.tables:
        Vertex.switch_table(name)
        return Vertex

    t = type(name, (object,), {'extend_existing': True, '__tablename__': name})
    user = Table(name, metadata,
                 Column('graph_id', Integer(), ForeignKey('tg_graphs.id')),
                 Column('eth', String(), primary_key=True),
                 Column('size', Float(precision=8)),
                 Column('pos', Geometry('Point', 3857))
                 )
    mapper(t, user)
    return t


class Vertex(Base):
    __tablename__ = "vertex_table"
    # __abstract__ = True

    graph_id = Column(Integer(), ForeignKey('tg_graphs.id'))
    eth = Column(String(), primary_key=True)
    size = Column(Float(precision=8))
    pos = Column(Geometry('Point', 3857))

    @staticmethod
    def switch_table(graph_name: str):
        Vertex.__tablename__ = graph_name
        Vertex.__table__ = graph_name

    @staticmethod
    def ensure_table_exists(table_name: str, db: object):
        query = """CREATE TABLE IF NOT EXISTS %(table_name)s
                (
                    graph_id   int,
                    eth        text UNIQUE PRIMARY KEY,
                    size       real,
                    pos        Geometry('Point', 3857),
                    CONSTRAINT fk_graph_id
                        FOREIGN KEY (graph_id)
                            REFERENCES tg_graphs (id)
                );"""
        engine.execute(query, {'table_name': AsIs(table_name)})

    @staticmethod
    def get_closest(x: float, y: float, db):
        query = f'SELECT graph_id, eth, size, ST_AsText(ST_PointFromWKB(pos)), pos <-> ST_SetSRID(ST_MakePoint({x}, {y}), 3857) AS dist ' \
                f'FROM {Vertex.__tablename__} ORDER BY dist LIMIT 1;'

        result = db.execute(query)
        closest = to_pd_frame(result)
        v = Vertex(graph_id=closest['graph_id'][0],
                   pos=wkt_to_x_y_list(closest['st_astext'][0]),
                   eth=closest['eth'][0],
                   size=closest['size'][0])
        return v

    @staticmethod
    def add_vertices(vertices: List[VertexInterface], graph_id: int):
        to_insert = []
        for v in vertices:
            p = 'POINT({} {})'.format(v['pos'][0], v['pos'][1])
            vertex = Vertex(eth=v['eth'], size=v['size'], pos=p, graph_id=graph_id)
            to_insert.append(vertex)
            # db.session.add(vertex)
        db.session.add_all(to_insert)
        db.session.commit()
        return []

    @staticmethod
    def get_in_list(eths: List[str], table_name: str, db: object) -> List[Vertex]:
        query = """SELECT graph_id, eth, size, ST_AsText(ST_PointFromWKB(pos)) AS pos FROM %(table_name)s WHERE %(table_name)s.eth IN %(eths)s;
        """
        raw_result = engine.execute(query, {'table_name': AsIs(table_name),
                                         'eths': tuple(eths)})
        db.commit()
        fetchall = to_pd_frame(raw_result)

        collect = []
        for (i, e) in fetchall.iterrows():
            pos_as_list = wkt_to_x_y_list(e['pos'])
            vertex = Vertex(graph_id=e['graph_id'], eth=e['eth'], size=e['size'], pos=pos_as_list)
            collect.append(vertex)
        return collect
