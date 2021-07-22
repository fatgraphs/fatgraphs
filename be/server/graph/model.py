from sqlalchemy import Integer, Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from be.server import Base
from be.server.graph.interface import GraphInterface


class Graph(Base):

    __tablename__ = "tg_graphs"

    id = Column(Integer(), primary_key=True)
    output_folder = Column(String(), default='')
    graph_name = Column(String())
    tile_size = Column(Integer())
    zoom_levels = Column(Integer())
    min_transparency = Column(Float(precision=8))
    max_transparency = Column(Float(precision=8))
    tile_based_mean_transparency = Column(Float(precision=8))
    std_transparency_as_percentage = Column(Float(precision=8))
    max_edge_thickness = Column(Float(precision=8))
    med_edge_thickness = Column(Float(precision=8))
    max_vertex_size = Column(Float(precision=8))
    med_vertex_size = Column(Float(precision=8))
    curvature = Column(Float(precision=8))
    bg_color = Column(String())
    source = Column(String())
    labels = Column(String())
    median_pixel_distance = Column(Float(precision=8))
    min = Column(Float(precision=8))
    max = Column(Float(precision=8))
    vertices = Column(Integer())
    edges = Column(Integer())

    def update(self, changes: GraphInterface):
        for key, val in changes.items():
            setattr(self, key, val)
        return self
