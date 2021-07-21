from sqlalchemy import Column, String, Integer

from be.server import Base


class VertexMetadata(Base):

    __tablename__ = "tg_vertex_metadata"

    id = Column(Integer(), primary_key=True)
    eth = Column(String())
    type = Column(String())
    label = Column(String())
    description = Column(String())
