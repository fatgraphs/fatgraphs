import random
from typing import List

from graph_tool import Edge
from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    select,
)
from sqlalchemy.orm import (
    joinedload,
    relationship,
)

from be.configuration import CONFIGURATIONS

from .. import (
    Base,
    SessionLocal,
)
from ..vertex import Vertex


class Edge(Base):

    __tablename__ = "tg_edge"

    graph_id = Column(Integer(), ForeignKey('tg_graphs.id'), primary_key=True)
    src_id = Column(String(), ForeignKey(Vertex.vertex), primary_key=True)
    trg_id = Column(String(), ForeignKey(Vertex.vertex), primary_key=True)
    src = relationship("Vertex", foreign_keys=[src_id], backref='outgoing_edges')
    trg = relationship("Vertex", foreign_keys=[trg_id], backref='incoming_edges')

    amount = Column(Float(precision=8))