from typing import List
import pandas as pd
from geoalchemy2 import Geometry, WKTElement
import geopandas as gpd
from be.configuration import SRID, VERTEX_TABLE_NAME
from .model import Vertex
from .. import engine
from ..graph.service import GraphService
from ..metadata.service import MetadataService

import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

class VertexService:

    @staticmethod
    def get_closest(graph_id: int, x: float, y: float, db) -> Vertex:
        table_name = VertexService.get_vertex_table_name(graph_id, db)
        Vertex.switch_table(table_name)
        closest = Vertex.get_closest(x, y, db)
        return closest

    @staticmethod
    def get_matching(graph_id: int, meta_type: str, meta_value: str, db: object) -> List[Vertex]:
        matches = MetadataService.get_by_type_and_value(meta_type, meta_value, db)
        eths = list(map(lambda e: e.eth_source, matches))
        by_eths = VertexService.get_by_eths(graph_id, eths, db)
        return by_eths

    @staticmethod
    def get_by_eths(graph_id: int, eths: List[str], db) -> List[Vertex]:
        if len(eths) == 0:
            return []
        table_name = VertexService.get_vertex_table_name(graph_id, db)
        closest = Vertex.get_in_list(eths, table_name, db)
        return closest

    @staticmethod
    def create(table_name: str, parsed_obj, db) -> List[Vertex]:

        # creating vertices opts out of the ORM
        # it seems very hard to use ORM for dynamically created tables

        geo_frame = VertexService.make_geoframe(parsed_obj)

        column_types = {'pos': Geometry('POINT', srid=SRID)}
        geo_frame.to_sql(table_name, engine, if_exists='append', index=False, dtype=column_types)

        return []


    @staticmethod
    def ensure_table_exists(table_name: str, db: object):
        Vertex.ensure_table_exists(table_name, db)

    @staticmethod
    def make_geoframe(parsed_obj):
        frame = pd.DataFrame(parsed_obj)
        geo_frame = gpd.GeoDataFrame(frame, geometry=gpd.points_from_xy(frame.x, frame.y))
        geo_frame = geo_frame.drop(columns=['x', 'y'])
        geo_frame = geo_frame.rename_geometry('pos')
        geo_frame['pos'] = geo_frame['pos'].apply(lambda x: WKTElement(x.wkt, srid=SRID))
        return geo_frame

    @staticmethod
    def get_vertex_table_name(graph_id: int, db):
        graph = GraphService.get_by_id(graph_id, db)
        graph_name = graph.graph_name
        vertex_table_name = VERTEX_TABLE_NAME(graph_name, graph_id)
        return vertex_table_name
