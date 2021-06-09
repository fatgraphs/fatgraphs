import geopandas as gpd
from geoalchemy2 import WKTElement

from be.configuration import SRID, METADATA_TABLE_NAME

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

    def save_frame_to_new_table(self, table_name, data_frame, column_types):
        data_frame.to_sql(table_name,
                          self.connection.engine,
                          index=False,
                          if_exists='replace',
                          dtype=column_types)

    def get_closest_point(self, x, y, table):
        query = f'SELECT eth, label, type, size, ST_AsText(ST_PointFromWKB(pos)), pos <-> ST_SetSRID(ST_MakePoint({x}, {y}), 3857) AS dist ' \
                f'FROM {table} ORDER BY dist LIMIT 1;'
        result = self.connection.execute_raw_query(query)
        return result

    def get_labelled_vertices(self, table_name):
        query = f'SELECT eth, ST_AsText(ST_PointFromWKB(pos)), label, type  FROM {table_name} WHERE label IS NOT NULL;'
        result = self.connection.execute_raw_query(query)
        return result

    def get_graph_metadata(self, graph_name):
        table_name = METADATA_TABLE_NAME(graph_name)
        query = f'SELECT * FROM {table_name};'
        result = self.connection.execute_raw_query(query)
        return result
