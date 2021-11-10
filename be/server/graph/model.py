from sqlalchemy import Integer, Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from be.server import Base
from be.server.gallery_categories import GalleryCategory
from be.server.graph.interface import GraphInterface


class Graph(Base):

    __tablename__ = "tg_graphs"

    id = Column(Integer(), primary_key=True)
    graph_name = Column(String())
    graph_category = Column(Integer(), ForeignKey(GalleryCategory.__table__.c.id))
    vertices = Column(Integer())
    edges = Column(Integer())

    def update(self, changes: GraphInterface):
        for key, val in changes.items():
            setattr(self, key, val)
        return self
