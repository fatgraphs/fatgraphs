import geopandas as gpd
from geoalchemy2 import WKTElement, Geometry
from sqlalchemy import String

from be.configuration import SRID

"""
Implements persistency logic 
"""
class Implementation():



    def __init__(self, db_connection):
        self.connection = db_connection

    def save_frame_to_new_table(self, table_name, data_frame, column_types):
        data_frame.to_sql(table_name,
                          self.connection.engine,
                          index=False,
                          if_exists='replace',
                          dtype=column_types)

    def to_geopandas(self, pandas_1):
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

    def query_closest_point(self, x, y, table):
        valorised_query = f'SELECT id, ST_AsText(ST_PointFromWKB(pos)), pos <-> ST_SetSRID(ST_MakePoint({x}, {y}), 3857) AS dist ' \
                          f'FROM {table} ORDER BY dist LIMIT 1;'
        result = self.connection.execute_raw_query(valorised_query)
        return list(result)[0]

    def get_where_equal(self, table_name, query_value, query_column):
        '''

        :param table_name: complete name of the table
        :param query_value: a value used as the RHS of an equality
        :param query_column: the complete name of the column in the spcecified table to match,
        to be  used as LHS of the equality
        :return: the rows where the equality is satisfied
        '''
        db_query_string = f'SELECT * FROM {table_name} WHERE {query_column} = {query_value};'
        result = self.connection.execute_raw_query(db_query_string)
        return list(result)

