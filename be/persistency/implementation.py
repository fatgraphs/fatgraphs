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


def toGeopandas(pandasFrame):
    # TODO generalise, parametrize column names for geometries
    """

    :param pandas_1: pandas frame
    :return: a geo pandas frame
    """
    sourceGeo = gpd.GeoDataFrame(pandasFrame,
                                  geometry=gpd.points_from_xy(pandasFrame.sourceX, pandasFrame.sourceY))
    sourceGeo = sourceGeo.rename_geometry('sourceGeo')
    targetGeo = gpd.GeoDataFrame(pandasFrame,
                                  geometry=gpd.points_from_xy(pandasFrame.targetX, pandasFrame.targetY))
    targetGeo = targetGeo.rename_geometry('targetGeo')
    geopandas2 = sourceGeo.merge(targetGeo).drop(columns=['sourceX', 'sourceY', 'targetX', 'targetY'])
    geopandas2['sourceGeo'] = geopandas2['sourceGeo'].apply(lambda x: WKTElement(x.wkt, srid=SRID))
    geopandas2['targetGeo'] = geopandas2['targetGeo'].apply(lambda x: WKTElement(x.wkt, srid=SRID))
    return geopandas2


class Implementation:
    """
    Methods here return the object that is the result of a query with the given dbLibrary.
    In the case of sqlalchemy (and geoSqlalchemy) such object is a cursor.
    """

    def __init__(self, dbConnection):
        self.connection = dbConnection

    def saveFrameToNewTable(self, tableName, dataFrame, columnTypes, ifExistsStrategy='replace'):
        dataFrame.to_sql(tableName,
                        self.connection.engine,
                        index=False,
                        if_exists=ifExistsStrategy,
                        dtype=columnTypes)

    def getClosestVertex(self, x, y, graphName):
        tableName = VERTEX_TABLE_NAME(graphName)
        query = f'SELECT eth, size, ST_AsText(ST_PointFromWKB(pos)), pos <-> ST_SetSRID(ST_MakePoint({x}, {y}), 3857) AS dist ' \
                f'FROM {tableName} ORDER BY dist LIMIT 1;'

        result = self.connection.executeRawQuery(query)
        return result

    def getLabelledVertices(self, graphName, searchMethod, searchQuery):

        query = """SELECT %(vertexTable)s.eth, ST_AsText(ST_PointFromWKB(pos)), %(type)s, %(label)s, %(vertexTable)s.size, id
                    FROM %(labelsTable)s
                    INNER JOIN  %(vertexTable)s ON  %(vertexTable)s.eth =  %(labelsTable)s.eth
                    WHERE %(searchQuery)s = %(labelsTable)s.%(searchMethod)s;
        """

        execute = self.connection.engine.execute(query,
                                                 {'labelsTable': AsIs(LABELS_TABLE),
                                                  'type': AsIs(LABELS_TABLE_TYPE),
                                                  'label': AsIs(LABELS_TABLE_LABEL),
                                                  'vertexTable': AsIs(VERTEX_TABLE_NAME(graphName)),
                                                  'searchQuery': searchQuery,
                                                  'searchMethod': AsIs(searchMethod)})
        return execute

    def getDistinctTypes(self):
        query = """SELECT DISTINCT type FROM %(tableName)s;"""
        result = self.connection.engine.execute(query, {'tableName': AsIs(LABELS_TABLE)})
        return result

    def getDistinctLabels(self):
        query = """SELECT DISTINCT label FROM %(tableName)s;"""
        result = self.connection.engine.execute(query, {'tableName': AsIs(LABELS_TABLE)})
        return result

    def getGraphMetadata(self, graphName):
        tableName = METADATA_TABLE_NAME(graphName)
        query = f"SELECT * FROM {tableName};"
        result = self.connection.executeRawQuery(query)
        return result

    def ensureUserDataTable(self):
        if not self.connection.isTablePresent(USER_TABLE):
            dataFrame = pd.DataFrame(data={'user_name': ['default_user'], 'recent_metadata_searches': ['']})
            self.saveFrameToNewTable(USER_TABLE, dataFrame, {'user_name': String,
                                                             'recent_metadata_searches': ARRAY(String, dimensions=2)})
            self.connection.addPrimaryKey(USER_TABLE, 'user_name')

    def ensureLabelsTableExists(self):
        if not self.connection.isTablePresent(LABELS_TABLE):
            dataFrame = pd.DataFrame(data={
                LABELS_TABLE_ETH: [],
                LABELS_TABLE_LABEL: [],
                LABELS_TABLE_TYPE: []})
            self.saveFrameToNewTable(LABELS_TABLE, dataFrame, {LABELS_TABLE_ETH: String,
                                                               LABELS_TABLE_LABEL: String,
                                                               LABELS_TABLE_TYPE: String})
            self.connection.createIndex(LABELS_TABLE, LABELS_TABLE_ETH)
            self.connection.createIndex(LABELS_TABLE, LABELS_TABLE_LABEL)
            self.connection.createIndex(LABELS_TABLE, LABELS_TABLE_TYPE)

    def getRecentTags(self):
        query = f'SELECT recent_metadata_searches FROM {USER_TABLE} WHERE user_name = \'default_user\';'
        result = self.connection.executeRawQuery(query)
        return result

    def updateRecentTags(self, tagsTagtypes):

        query = """
            INSERT INTO %(table)s (user_name, recent_metadata_searches)
            VALUES(%(userName)s, %(values)s)
            ON CONFLICT (user_name) DO UPDATE
            SET recent_metadata_searches = EXCLUDED.recent_metadata_searches;
        """
        result = self.connection.engine.execute(query,
                                                {"table": AsIs(USER_TABLE),
                                                 "userName": 'default_user',
                                                 "values": tagsTagtypes})
        return result

    def saveGraphMetadata(self, graphMetadata):
        graphName = graphMetadata.getGraphName()
        tableName = METADATA_TABLE_NAME(graphName)
        metadataFrame = graphMetadata.getSingleFrame()
        self.saveFrameToNewTable(tableName, metadataFrame, {})

    def addVertexMetadata(self, eth, metadataValue, metadataType):
        query = """INSERT INTO %(labelsTable)s VALUES (%(eth)s, %(label)s, %(type)s);
        """
        result = self.connection.engine.execute(query,
                                                {"labelsTable": AsIs(LABELS_TABLE),
                                                 'eth': eth,
                                                 'label': metadataValue if metadataType == 'label' else '\'\'',
                                                 'type': metadataValue if metadataType == 'type' else '\'\''})
        return result
