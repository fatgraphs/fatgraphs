import pandas as pd
from flask_restx import abort
from marshmallow import Schema
from sqlalchemy import inspect


def to_pd_frame(raw_result):
    """
    :param raw_result: the object returned from executing a raw query with sqlAlchemy
    :return: a pandas frame where the column names are the DB column names and the rows are DB records
    """
    df = pd.DataFrame(raw_result.fetchall())
    if df.empty:
        return df
    df.columns = raw_result.keys()
    return df



def wkt_to_x_y_list(wkt):
    """

    :param wkt: well known text representation of a 2D POINT (a point in GIS).
            e.g. POINT(34234 42)
    :return: a python list where the first element is the x and the second is the y
    """
    p = wkt.split('(')[-1].split(')')[0].split(' ')
    return [float(p[0]), float(p[1])]


class CamelCaseSchema(Schema):
    """Schema that uses camel-case for its external representation
    and snake-case for its internal representation.

    Needed because Python is traditionally snake_case but JS is camelCase
    """

    def camelcase(self, s):
        parts = iter(s.split("_"))
        return next(parts) + "".join(i.title() for i in parts)

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = self.camelcase(field_obj.data_key or field_name)


def is_table_present(tableName, engine):
    '''

    :param tableName:
    :return: True if the engine contains table with an equal name
    '''
    return inspect(engine).has_table(tableName)

def is_column_present(tableName, columnName, engine):
    """
    :param tableName:
    :param columnName:
    :return: True if  the table contains a column with the specified name
    """
    if not is_table_present(tableName, engine):
        return False
    # TODO use session
    with engine.connect() as con:
        query = """ SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name=%(tableName)s and column_name=%(columnName)s;"""

        result = con.execute(query, {'tableName': tableName, 'columnName': columnName})
        return result.rowcount != 0