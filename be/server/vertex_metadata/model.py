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
    """
    Vertex (e.g. eth address) not usd as primary key as there could be duplicates
    """

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
        
    @staticmethod
    def delete(vertex, typee, value, db):
        query = text(
            """
            UPDATE :type_label_table 
            SET :type_or_label = ''
            WHERE vertex = :vertex AND :type_or_label = :value; 
            """
        )

        with engine.connect() as conn:
            result = conn.execute(
                query, 
                {
                    'type_label_table': AsIs(VertexMetadata.__tablename__),
                    'type_or_label': AsIs(typee),
                    'vertex': vertex,
                    'value': value
                }
            )
            return result

    @staticmethod
    def from_row(row):
        result = VertexMetadata(vertex=row[1]['vertex'],
            type=row[1]['type'],
            label=row[1]['label'],
            account_type=int(row[1]['account_type']),
            description=row[1]['description'],
            # id = row[1]['id'],
        )
        return result

    def __eq__(self, other):
        if not isinstance(other, VertexMetadata):
            return False
        return self.vertex == other.vertex and\
            self.type == other.type and\
            self.label == other.label and\
            self.account_type == other.account_type and\
            self.description == other.description
