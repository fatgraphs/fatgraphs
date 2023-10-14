
from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
)
from sqlalchemy.orm import (
    relationship,
)


from .. import (
    Base,
)
from ..vertex import Vertex


class Edge(Base):

    __tablename__ = "tg_edge"

    graph_id = Column(Integer(), ForeignKey('tg_graphs.id'), primary_key=True)
    src_id = Column(String(), ForeignKey(Vertex.vertex), primary_key=True)
    trg_id = Column(String(), ForeignKey(Vertex.vertex), primary_key=True)
    src = relationship(
        "Vertex", 
        viewonly=True, 
        foreign_keys=[src_id, graph_id]
    )
    trg = relationship(
        "Vertex", 
        viewonly=True, 
        foreign_keys=[trg_id, graph_id]
    )

    # composite FKs needs the ForeignKeyConstraint to work properly
    __table_args__ = (
        ForeignKeyConstraint(
            [src_id, graph_id],
            [Vertex.vertex, Vertex.graph_id]
        ),
        ForeignKeyConstraint(
            [trg_id, graph_id],
            [Vertex.vertex, Vertex.graph_id]
        ),
    )

    amount = Column(Float(precision=8))