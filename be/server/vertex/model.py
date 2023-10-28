from geoalchemy2 import Geometry
from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
)

from be.server import (
    Base,
)
from be.server.utils import (
    wkt_to_x_y_list,
)


class Vertex(Base):

    __tablename__ = "tg_vertex"

    graph_id = Column(
        Integer(), 
        ForeignKey('tg_graphs.id'), 
        primary_key=True,
    )
    vertex = Column(
        String(), 
        primary_key=True,
    )
    size = Column(Float(precision=8))
    pos = Column(Geometry('Point', 3857))

    @staticmethod
    def from_dict(obj):
        return Vertex(
            graph_id=obj.graph_id,
            vertex=obj.vertex,
            size=obj.size,
            pos=obj.pos
        )

    @staticmethod
    def _map_to_model(fetchall):
        collect = []
        for (i, e) in fetchall.iterrows():
            pos_as_list = wkt_to_x_y_list(e['pos'])
            vertex = Vertex(graph_id=e['graph_id'], vertex=e['vertex'], size=e['size'], pos=pos_as_list)
            collect.append(vertex)
        return collect
