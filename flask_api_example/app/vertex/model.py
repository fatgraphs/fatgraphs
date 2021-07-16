from app import db  # noqa
from geoalchemy2 import Geometry
from sqlalchemy import Integer, Column, String, Float

from be.configuration import VERTEX_TABLE_NAME
from ..utils import to_pd_frame, wkt_to_x_y_list


class Vertex(db.Model):

    __tablename__ = "me_vertex"

    @staticmethod
    def switch_table(graph_name: str):
        __tablename__ = graph_name

    @staticmethod
    def getClosest(graph_name: str, x: float, y: float):
        table_name = VERTEX_TABLE_NAME(graph_name)
        Vertex.switch_table(table_name)
        query = f'SELECT id, eth, size, ST_AsText(ST_PointFromWKB(pos)), pos <-> ST_SetSRID(ST_MakePoint({x}, {y}), 3857) AS dist ' \
                f'FROM {table_name} ORDER BY dist LIMIT 1;'

        result = db.session.execute(query)
        closest = to_pd_frame(result)
        v = Vertex()
        v.id = closest['id'][0]
        v.pos = wkt_to_x_y_list(closest['st_astext'][0])
        v.eth = closest['eth'][0]
        v.size = closest['size'][0]
        return v

    id = Column(Integer(), primary_key=True)
    # graph_id = Column(Integer(), ForeignKey('tg_graphs.id'))
    # metadata =  Column(Integer(), ForeignKey('tg_graphs.id'))
    eth = Column(String())
    size = Column(Float(precision=8))
    pos = Column(Geometry('Point', 3857))
