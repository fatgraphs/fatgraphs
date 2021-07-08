from psycopg2._psycopg import AsIs
from sqlalchemy import text, create_engine, inspect

"""
Holds the connection object to the DB.
Allows execution of raw sql queries
"""


class DbConnection():

    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)

    def execute_raw_query(self, query):
        query_text = text(query)
        result = self.engine.execute(query_text)
        return result

    def add_primary_key(self, table_name, key):
        with self.engine.connect() as con:
            con.execute(f'ALTER TABLE {table_name} ADD PRIMARY KEY ({key});')

    def create_index(self, table_name, column_name):
        if not self.is_column_present(table_name, column_name):
            raise Exception(f'Trying to create an index on a column ({column_name}) '
                            f'that is not present on the specified table ({table_name}')
        with self.engine.connect() as con:
            query = """CREATE INDEX %(index_name)s ON %(table_name)s(%(column_name)s)"""
            con.execute(query, {"index_name": AsIs(column_name + '_index'),
                                "table_name": AsIs(table_name),
                                "column_name": AsIs(column_name)})

    def is_table_present(self, table_name):
        '''

        :param table_name:
        :return: True if the engine contains table with an equal name
        '''
        return inspect(self.engine).has_table(table_name)

    def is_column_present(self, table_name, column_name):
        """
        :param table_name:
        :param column_name:
        :return: True if  the table contains a column with the specified name
        """
        if not self.is_table_present(table_name):
            return False
        with self.engine.connect() as con:
            query = """ SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name=%(table_name)s and column_name=%(column_name)s;"""

            result = con.execute(query, {'table_name': table_name, 'column_name': column_name})
            return result.rowcount != 0
