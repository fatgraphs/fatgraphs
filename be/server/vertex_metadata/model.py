import pandas as pd
from psycopg2._psycopg import AsIs
from sqlalchemy import (
    Column,
    ForeignKeyConstraint,
    Integer,
    String,
)

from be.server import engine
from be.server.utils import to_pd_frame
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship

from be.server.vertex.model import Vertex

from .. import (
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
