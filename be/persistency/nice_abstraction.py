from be.configuration import DB_USER_NAME, DB_PASSWORD, DB_URL, DB_NAME, METADATA_TABLE_NAME, \
    ID_TABLE_NAME, VERTEX_TABLE_NAME, SRID
from be.persistency.db_connection import DbConnection
from be.persistency.implementation import Implementation
from geoalchemy2 import Geometry
from sqlalchemy import String
import pandas as pd

"""
This class exposes the methods that are used to interact with the persistency layer, 
hiding the detail in the implementaiton.
"""
class NiceAbstraction:

    def __init__(self, connection_string):
        self.connection = DbConnection(connection_string)
        self.impl = Implementation(self.connection)

    def create_id_to_eth_table(self, graph_name, id_to_eth):
        table_name = ID_TABLE_NAME(graph_name)
        id_to_eth = id_to_eth.rename(columns={'vertex': 'id'})
        self.impl.save_frame_to_new_table(table_name, id_to_eth, {})

    def create_metadata_table(self, graph_name, graph_metadata):
        table_name = METADATA_TABLE_NAME(graph_name)
        self.impl.save_frame_to_new_table(table_name, graph_metadata, {})

    def create_vertex_table(self, graph_name, layout):
        # TODO now only positions ae saved, in the future this table will contain ALL info related to vertices (degree, size, shape, label ...)
        table_name = VERTEX_TABLE_NAME(graph_name)
        geopandas_frame = self.impl.to_geopandas(layout.edge_ids_to_positions.to_pandas())

        s = geopandas_frame[['source_id', 'source_geo']].rename(columns={'source_id': 'id', 'source_geo': 'pos'})
        t = geopandas_frame[['target_id', 'target_geo']].rename(columns={'target_id': 'id', 'target_geo': 'pos'})
        geopandas_frame = pd.concat([s, t], axis=0).drop_duplicates()
        all_in_one_frame = geopandas_frame
        column_types = {'pos': Geometry('POINT', srid=SRID)}
        self.impl.save_frame_to_new_table(table_name, all_in_one_frame, column_types)

    def get_eth(self, graph_name, vertex_id):
        return self.impl.get_where_equal(ID_TABLE_NAME(graph_name), vertex_id, 'id')[0][1]

    def get_closest_point(self, x, y, table):
        return self.impl.query_closest_point(x, y, table)

singletonNiceAbstraction = NiceAbstraction(f'postgresql://{DB_USER_NAME}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}')