from psycopg2._psycopg import AsIs
from sqlalchemy import text, create_engine, inspect

"""
Holds the connection object to the DB.
Allows execution of raw sql queries
"""


class DbConnection:

    def __init__(self, connectionString):
        self.engine = create_engine(connectionString)

    def executeRawQuery(self, query):
        queryText = text(query)
        result = self.engine.execute(queryText)
        return result

    def addPrimaryKey(self, tableName, key):
        with self.engine.connect() as con:
            con.execute(f'ALTER TABLE {tableName} ADD PRIMARY KEY ({key});')

    def createIndex(self, tableName, columnName):
        if not self.is_column_present(tableName, columnName):
            raise Exception(f'Trying to create an index on a column ({columnName}) '
                            f'that is not present on the specified table ({tableName}')
        with self.engine.connect() as con:
            query = """CREATE INDEX %(indexName)s ON %(tableName)s(%(columnName)s)"""
            con.execute(query, {"indexName": AsIs(columnName + '_index'),
                                "tableName": AsIs(tableName),
                                "columnName": AsIs(columnName)})

    def isTablePresent(self, tableName):
        '''

        :param tableName:
        :return: True if the engine contains table with an equal name
        '''
        return inspect(self.engine).has_table(tableName)

    def isColumnPresent(self, tableName, columnName):
        """
        :param tableName:
        :param columnName:
        :return: True if  the table contains a column with the specified name
        """
        if not self.isTablePresent(tableName):
            return False
        with self.engine.connect() as con:
            query = """ SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name=%(tableName)s and column_name=%(columnName)s;"""

            result = con.execute(query, {'tableName': tableName, 'columnName': columnName})
            return result.rowcount != 0
