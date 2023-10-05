import warnings
from typing import List

from psycopg2._psycopg import AsIs
from sqlalchemy import func

from be.configuration import VERTEX_GLOBAL_TABLE
from be.server.utils import wkt_to_x_y_list
from .model import Vertex
from .. import engine
from ..vertex_metadata.service import VertexMetadataService
from sqlalchemy.sql import text
from sqlalchemy.orm import aliased

warnings.simplefilter(action='ignore', category=UserWarning)


class VertexService:

    @staticmethod
    def get_closest(graph_id: int, x: float, y: float, session) -> Vertex:

        query_point = func.ST_SetSRID(
            func.ST_MakePoint(x, y),
            3857
        )
    
        closest_vertex = (
            session.query(
                Vertex.graph_id,
                Vertex.vertex,
                Vertex.size,
                func.ST_PointFromWKB(Vertex.pos).label('pos'),
                func.ST_Distance(
                    query_point,
                    func.ST_Transform(Vertex.pos, 3857)
                ).label('distance')
            )
            .filter(Vertex.graph_id == graph_id)
            .order_by('distance')
            .first()
        )

        return closest_vertex
           

    @staticmethod
    def get_by_eths(graph_id: int, eths: List[str], db) -> List[Vertex]:

        if len(eths) == 0:
            return []
        vertices = Vertex.get(eths, graph_id, db)
        return vertices

    @staticmethod
    def ensure_vertex_table_exists(table_name: str, graph_id: int, db):

        query = text(
            """
            CREATE TABLE IF NOT EXISTS :table_name 
            PARTITION OF :vertex_table
            FOR VALUES IN :graph_id;
            """
        )

        with db.get_bind().connect() as conn:
            trans = conn.begin()

            conn.execute(
                query, 
                {
                    'table_name': AsIs(table_name),
                    'vertex_table': AsIs(VERTEX_GLOBAL_TABLE),
                    'graph_id': tuple([str(graph_id)])
                }
            )

            trans.commit()

    @staticmethod
    def attach_metadata(vertices, db):
        if not isinstance(vertices, list):
            vertices = [vertices]
        for v in vertices:
            metadata = VertexMetadataService.get_by_eth(v.vertex, db)
            for m in metadata:
                for attr in ['types', 'labels']:
                    existing = getattr(v, attr, [])
                    existing.append(getattr(m, attr[0:-1]))
                    setattr(v, attr, existing)
        return vertices

    @staticmethod
    def get_by_type(graph_id, type, db):
        global_matches = VertexMetadataService.get_by_type(type, db)
        if graph_id is not None:
            global_eths = list(map(lambda e: e.vertex, global_matches))
            this_graph_matches = VertexService.get_by_eths(graph_id, global_eths, db)
            return this_graph_matches
        return global_matches

    @staticmethod
    def get_by_label(graph_id, label, db):
        global_matches = VertexMetadataService.get_by_label(label, db)
        if graph_id is not None:
            global_eths = list(map(lambda e: e.vertex, global_matches))
            this_graph_matches = VertexService.get_by_eths(graph_id, global_eths, db)
            return this_graph_matches
        return global_matches

    @staticmethod
    def get_by_eth_across_graphs(eth, db):
        return Vertex.get([eth], None, db)

