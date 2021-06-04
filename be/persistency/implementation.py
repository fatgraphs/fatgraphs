import geopandas as gpd
from geoalchemy2 import WKTElement, Geometry
from sqlalchemy import String

"""
Implements persistency logic 
"""
class Implementation():

    SRID = 3857

    def __init__(self, db_connection):
        self.connection = db_connection

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
        geopandas_2['source_geo'] = geopandas_2['source_geo'].apply(lambda x: WKTElement(x.wkt, srid=3857))
        geopandas_2['target_geo'] = geopandas_2['target_geo'].apply(lambda x: WKTElement(x.wkt, srid=3857))
        return geopandas_2

    def persist_geoframe(self, geo_frame, destination_table):
        # TODO generalise, parametrize column names for geometries
        geo_frame.to_sql(destination_table,
                         self.connection.engine,
                         if_exists='append',
                         index=False,
                         dtype={'source_geo': Geometry('POINT', srid=Implementation.SRID),
                                'target_geo': Geometry('POINT', srid=Implementation.SRID),
                                'source_eth': String(42),
                                'target_eth': String(42)})

    def query_closest_point(self, x, y, table):
        valorised_query = "SELECT source_eth, ST_AsText(ST_PointFromWKB(source_geo)), source_geo <-> ST_SetSRID(ST_MakePoint({0}, {1}), 3857) AS dist " \
                          "FROM {2} " \
                          "ORDER BY dist LIMIT 1;".format(x, y, table)
        result = self.connection.execute_raw_query(valorised_query)
        return list(result)[0]
