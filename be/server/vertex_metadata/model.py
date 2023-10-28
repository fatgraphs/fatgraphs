from sqlalchemy import (
    Column,
    ForeignKeyConstraint,
    Integer,
    String,
)

from sqlalchemy.orm import relationship

from be.server.vertex.model import Vertex

from be.server import (
    Base,
)

class VertexMetadata(Base):

    __tablename__ = "tg_vertex_metadata"

    id = Column(
        Integer(), 
        primary_key=True,
    )
    graph_id = Column(
        Integer(), 
    )
    vertex = Column(
        String(), 
    )
    type = Column(
        String(), 
    )
    label = Column(
        String(), 
    )
    account_type = Column(
        Integer(), 
    )
    description = Column(
        String(), 
    )
    icon = Column(
        String(), 
    )

    vertex_obj = relationship(
        "Vertex", 
        backref='metadata_objs', 
        foreign_keys=[vertex, graph_id]
    )

    __table_args__ = (
        ForeignKeyConstraint(
            [vertex, graph_id],
            [Vertex.vertex, Vertex.graph_id]
        ),
    )

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
