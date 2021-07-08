import geopandas as gpd
import pandas as pd
from geoalchemy2 import WKTElement
from psycopg2._psycopg import AsIs
from sqlalchemy import String, ARRAY

from be.configuration import SRID, METADATA_TABLE_NAME, USER_TABLE, VERTEX_TABLE_NAME, LABELS_TABLE, LABELS_TABLE_ETH, \
    LABELS_TABLE_LABEL, LABELS_TABLE_TYPE

"""
Implements persistency logic 
"""


def to_geopandas(pandas_1):
    # TODO generalise, parametrize column names for geometries
    """

    :param pandas_1: pandas frame
    :return: a geo pandas frame
    """
    source_geo = gpd.GeoDataFrame(pandas_1,
                                  geometry=gpd.points_from_xy(pandas_1.source_x, pandas_1.source_y))
    source_geo = source_geo.rename_geometry('source_geo')
    target_geo = gpd.GeoDataFrame(pandas_1,
                                  geometry=gpd.points_from_xy(pandas_1.target_x, pandas_1.target_y))
    target_geo = target_geo.rename_geometry('target_geo')
    geopandas_2 = source_geo.merge(target_geo).drop(columns=['source_x', 'source_y', 'target_x', 'target_y'])
    geopandas_2['source_geo'] = geopandas_2['source_geo'].apply(lambda x: WKTElement(x.wkt, srid=SRID))
    geopandas_2['target_geo'] = geopandas_2['target_geo'].apply(lambda x: WKTElement(x.wkt, srid=SRID))
    return geopandas_2


class Implementation:
    """
    Methods here return the object that is the result of a query with the given dbLibrary.
    In the case of sqlalchemy (and geoSqlalchemy) such object is a cursor.
    """

    def __init__(self, db_connection):
        self.connection = db_connection

    def save_frame_to_new_table(self, table_name, data_frame, column_types, if_exists_strategy='replace'):
        data_frame.to_sql(table_name,
                          self.connection.engine,
                          index=False,
                          if_exists=if_exists_strategy,
                          dtype=column_types)

    def get_closest_vertex(self, x, y, graph_name):
        table_name = VERTEX_TABLE_NAME(graph_name)
        query = f'SELECT eth, size, ST_AsText(ST_PointFromWKB(pos)), pos <-> ST_SetSRID(ST_MakePoint({x}, {y}), 3857) AS dist ' \
                f'FROM {table_name} ORDER BY dist LIMIT 1;'

        result = self.connection.execute_raw_query(query)
        return result

    def get_labelled_vertices(self, graph_name, search_method, search_query):

        query = """SELECT %(labels_table)s.eth, ST_AsText(ST_PointFromWKB(pos)), %(type)s, %(label)s, %(vertex_table)s.size
                    FROM %(labels_table)s
                    INNER JOIN  %(vertex_table)s ON  %(vertex_table)s.eth =  %(labels_table)s.eth
                    WHERE %(search_query)s = %(labels_table)s.%(search_method)s;
        """

        execute = self.connection.engine.execute(query,
                                                 {'labels_table': AsIs(LABELS_TABLE),
                                                  'type':AsIs(LABELS_TABLE_TYPE),
                                                  'label': AsIs(LABELS_TABLE_LABEL),
                                                  'vertex_table': AsIs(VERTEX_TABLE_NAME(graph_name)),
                                                  'search_query': search_query,
                                                  'search_method': AsIs(search_method)})

        # query = f'SELECT {LABELS_TABLE}.eth, ST_AsText(ST_PointFromWKB(pos)), {LABELS_TABLE_TYPE}, {LABELS_TABLE_LABEL}, {table_name}.size, id ' \
        #         f'FROM {LABELS_TABLE} ' \
        #         f'INNER JOIN {table_name} ON {table_name}.eth = {LABELS_TABLE}.eth '
        #
        # if search_method == 'eth':
        #     query += f'WHERE \'{search_query}\' = {LABELS_TABLE}.{search_method};'
        # else:
        #     query += f'WHERE \'{search_query}\' = ANY({LABELS_TABLE}.{search_method});'

        # result = self.connection.execute_raw_query(query)
        return execute

    def get_distinct_types(self):
        query = """SELECT DISTINCT type FROM %(table_name)s;"""
        result = self.connection.engine.execute(query, {'table_name': AsIs(LABELS_TABLE)})
        return result

    def get_distinct_labels(self):
        query = """SELECT DISTINCT label FROM %(table_name)s;"""
        result = self.connection.engine.execute(query, {'table_name': AsIs(LABELS_TABLE)})
        return result

    def get_graph_metadata(self, graph_name):
        table_name = METADATA_TABLE_NAME(graph_name)
        query = f"SELECT * FROM {table_name};"
        result = self.connection.execute_raw_query(query)
        return result

    def ensure_user_data_table(self):
        if not self.connection.is_table_present(USER_TABLE):
            data_frame = pd.DataFrame(data={'user_name': ['default_user'], 'last_search_tags': ['']})
            self.save_frame_to_new_table(USER_TABLE, data_frame, {'user_name': String,
                                                                  'last_search_tags': ARRAY(String, dimensions=2)})
            self.connection.add_primary_key(USER_TABLE, 'user_name')

    def ensure_labels_table_exists(self):
        if not self.connection.is_table_present(LABELS_TABLE):
            data_frame = pd.DataFrame(data={
                LABELS_TABLE_ETH: [],
                LABELS_TABLE_LABEL: [],
                LABELS_TABLE_TYPE: []})
            self.save_frame_to_new_table(LABELS_TABLE, data_frame, {LABELS_TABLE_ETH: String,
                                                                    LABELS_TABLE_LABEL: String,
                                                                    LABELS_TABLE_TYPE: String})
            self.connection.create_index(LABELS_TABLE, LABELS_TABLE_ETH)
            self.connection.create_index(LABELS_TABLE, LABELS_TABLE_LABEL)
            self.connection.create_index(LABELS_TABLE, LABELS_TABLE_TYPE)

    def get_recent_tags(self):
        query = f'SELECT last_search_tags FROM {USER_TABLE} WHERE user_name = \'default_user\';'
        result = self.connection.execute_raw_query(query)
        return result

    def update_recent_tags(self, tags_tagtypes):

        query = """
            INSERT INTO %(table)s (user_name, last_search_tags)
            VALUES(%(user_name)s, %(values)s)
            ON CONFLICT (user_name) DO UPDATE
            SET last_search_tags = EXCLUDED.last_search_tags;
        """
        result = self.connection.engine.execute(query,
                                                {"table": AsIs(USER_TABLE),
                                                 "user_name": 'default_user',
                                                 "values": tags_tagtypes})
        return result

    def save_graph_metadata(self, graph_metadata):
        graph_name = graph_metadata.get_graph_name()
        table_name = METADATA_TABLE_NAME(graph_name)
        metadata_frame = graph_metadata.get_single_frame()
        self.save_frame_to_new_table(table_name, metadata_frame, {})
