from psycopg2._psycopg import AsIs
from sqlalchemy import Column, String, Integer

from be.server import Base, engine


class VertexMetadata(Base):

    __tablename__ = "tg_vertex_metadata"

    id = Column(Integer(), primary_key=True)
    eth = Column(String())
    type = Column(String())
    label = Column(String())
    description = Column(String())

    @staticmethod
    def merge_for_account_types(graph_vertex_table_name: str):
        query = """SELECT * FROM %(graph_vertex_table_name)s 
        INNER JOIN %(tg_account_type)s 
        ON %(tg_account_type)s.vertex = %(graph_vertex_table_name)s.eth"""

        raw_result = engine.execute(query, {
            'graph_vertex_table_name': AsIs(graph_vertex_table_name),
            'tg_account_type': 'tg_account_type'
            })

