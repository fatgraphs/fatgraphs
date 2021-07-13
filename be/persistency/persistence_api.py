import pandas as pd
from geoalchemy2 import Geometry
from sqlalchemy import String

from be.configuration import DB_USER_NAME, DB_PASSWORD, DB_URL, DB_NAME, METADATA_TABLE_NAME, VERTEX_TABLE_NAME, SRID, \
    LABELS_TABLE
from be.persistency.db_connection import DbConnection
from be.persistency.implementation import Implementation, toGeopandas

"""
This class exposes the methods that are used to interact with the persistency layer, 
hiding the detail in the implementaiton.
"""


def toPdFrame(rawResult):
    """
    :param raw_result: the object returned from executing a raw query with sqlAlchemy
    :return: a pandas frame where the column names are the DB column names and the rows are DB records
    """
    df = pd.DataFrame(rawResult.fetchall())
    if df.empty:
        return df
    df.columns = rawResult.keys()
    return df


class PersistenceAPI:
    '''
    Mehtods of here should return results that are easy to work with: either primitive types or pandas frames.
    '''

    instantiated = False

    def __init__(self, connection_string):
        if PersistenceAPI.instantiated:
            raise Exception("PersistenceAPI is a singleton, some parts of the code are initialising it twice")
        PersistenceAPI.instantiated = True
        self.connection = DbConnection(connection_string)
        self.impl = Implementation(self.connection)

    def ensureUserTableExists(self):
        # TODO assumed one user for now
        """
        If table with  user preferences doesnt exists it creates it.
        It also makes the user_name a primary key.
        """
        self.impl.ensureUserDataTable()

    def ensureLabelsTableExists(self):
        self.impl.ensureLabelsTableExists()

    def updateRecentMetadataSearches(self, metadataObject):
        """
        Updates the recently searched metadata of the default user.

        :param metadata_object:the latest metadata queried by a user
        :param tag_list_as_string:
        :return:
        """
        def insertNewItem(df, metadataObject):
            current = df['recent_metadata_searches'].values[0]
            if len(current) == 0:
                current = [[], []]
            current[0].insert(0, metadataObject['metadata_value'])
            current[1].insert(0, metadataObject['metadata_type'])
            updated = [[], []]
            updated[0] = current[0][0:5]
            updated[1] = current[1][0:5]
            return updated

        oldMetadataSearches = self.getRecentMetadataSearches()
        newMetadataSearches = insertNewItem(oldMetadataSearches, metadataObject)
        self.impl.updateRecentTags(newMetadataSearches)

    def getRecentMetadataSearches(self):
        raw_result = self.impl.getRecentTags()
        df = toPdFrame(raw_result)
        return df

    def createMetadataTable(self, graphMetadata):
        self.impl.saveGraphMetadata(graphMetadata)

    def createVertexTable(self, graphName, layout, idToEth):
        # TODO now only positions ae saved, in the future this table will contain ALL info related to vertices (degree, size, shape, label ...
        # TODO refactor
        tableName = VERTEX_TABLE_NAME(graphName)
        geopandasFrame = toGeopandas(layout.edgeIdsToPositions.to_pandas())

        # all vertex IDS to position
        s = geopandasFrame[['sourceId', 'sourceGeo']].rename(columns={'sourceId': 'id', 'sourceGeo': 'pos'})
        t = geopandasFrame[['targetId', 'targetGeo']].rename(columns={'targetId': 'id', 'targetGeo': 'pos'})
        geopandasFrame = pd.concat([s, t], axis=0).drop_duplicates()

        # id to eth address
        idToEth = idToEth.rename(columns={'vertex': 'id', 'address': 'eth'})
        allInOneFrame = geopandasFrame.merge(idToEth, on='id')

        # TODO: this is a quick fix, understand why they need to be reordered.
        # Consider keeping layout.vertex_sizes as a pandas frame instead of a list so merge can  be used
        allInOneFrame = allInOneFrame.sort_values(['id']).reset_index(drop=True)
        allInOneFrame['size'] = layout.vertexSizes
        columnTypes = {'pos': Geometry('POINT', srid=SRID)}
        self.impl.saveFrameToNewTable(tableName, allInOneFrame, columnTypes)

    def createEdgeTable(self):
        # TODO
        pass

    def getClosestVertex(self, x, y, graphName):
        rawResult = self.impl.getClosestVertex(x, y, graphName)
        df = toPdFrame(rawResult)
        return df

    def getGraphMetadata(self, graphName):
        raw_result = self.impl.getGraphMetadata(graphName)
        df = toPdFrame(raw_result)
        return df

    def getLabelledVertices(self, graphName, searchMethod, searchQuery):
        rawResult = self.impl.getLabelledVertices(graphName, searchMethod, searchQuery)
        df = toPdFrame(rawResult)
        return df

    def getAllTypesAndLabels(self):
        rawResult = self.impl.getDistinctTypes()
        df = toPdFrame(rawResult)
        rawResult = self.impl.getDistinctLabels()
        df = toPdFrame(rawResult).append(df)
        return df

    def isGraphInDb(self, graphName):
        # TODO add edge_table
        tablesMustExist = [VERTEX_TABLE_NAME(graphName),
                             METADATA_TABLE_NAME(graphName)]
        return all(
            list(map(
                lambda table_name: self.connection.isTablePresent(table_name),
                tablesMustExist
            ))
        )

    def populateLabelsTable(self, frame):
        self.impl.saveFrameToNewTable(LABELS_TABLE,
                                          frame,
                                          {'eth': String,
                                           'label': String,
                                           'type': String},
                                          ifExistsStrategy='append')

    def addVertexMetadata(self, eth, metadataValue, metadataType):
        rawResult = self.impl.addVertexMetadata(eth, metadataValue, metadataType)


# only one instance
persistenceApi = PersistenceAPI(f'postgresql://{DB_USER_NAME}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}')
