
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

    def is_table_present(self, table_name):
        '''

        :param table_name:
        :return: True if the engine contains table with an equal name
        '''
        return inspect(self.engine).has_table(table_name)
