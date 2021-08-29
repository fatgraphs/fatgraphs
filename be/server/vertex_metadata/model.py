from typing import List
from psycopg2._psycopg import AsIs
from sqlalchemy import Column, String, Integer

from be.server import Base, engine
from be.server.searches import AUTOCOMPLETE_TERMS_PER_PAGE
from be.server.utils import to_pd_frame
import pandas as pd

class VertexMetadata:
    """
    Vertex (e.g. eth address) not usd as primary key as there could be diplicates
    """

    __type_labels__ = "tg_vertex_metadata"
    __account_type__ = "tg_account_type"

    def __init__(self,
        eth: str,
        type: str = None,
        label: str = None,
        account_type: int = None,
        description: str = None,
        id: int = None,):

        self.id = id
        self.eth = eth
        self.type = type
        self.label = label
        self.account_type = account_type
        self.description = description


    @staticmethod
    def merge_for_account_types(graph_vertex_table_name: str):
        query = """SELECT * FROM %(graph_vertex_table_name)s 
        INNER JOIN %(tg_account_type)s 
        ON %(tg_account_type)s.vertex = %(graph_vertex_table_name)s.eth"""

        raw_result = engine.execute(query, {
            'graph_vertex_table_name': AsIs(graph_vertex_table_name),
            'tg_account_type': 'tg_account_type'
            })


    @staticmethod
    def filter_by(db: object, eth=None, type=None, label=None):
        query = """SELECT * FROM  %(type_label_table)s """
        substitution = {'type_label_table': AsIs(VertexMetadata.__type_labels__)}
        if eth != None:
            query = query + """WHERE %(type_label_table)s.eth = %(eth)s """
            substitution['eth'] = eth

        if type != None:
            query = query + """WHERE  %(type_label_table)s.type =  %(type)s """
            substitution['type'] = type

        if label != None:
            query = query + """WHERE  %(type_label_table)s.label =  %(label)s """
            substitution['label'] = label

        query = query + ';'

        result = db.bind.engine.execute(query, substitution)

        from_type_label_table = to_pd_frame(result)
        if from_type_label_table.empty:
            return []
        account_types = pd.DataFrame()
        for eth_ in list(set(from_type_label_table['eth'].values)):
            query = """SELECT * FROM %(account_table)s WHERE %(account_table)s.vertex = %(eth)s"""
            result = db.bind.engine.execute(query, {
                'account_table': AsIs(VertexMetadata.__account_type__),
                'eth': eth_})
            frame = to_pd_frame(result)
            account_types = account_types.append(frame)

        from_type_label_table = from_type_label_table.merge(account_types.rename(columns={'type': 'account_type'}), left_on='eth', right_on='vertex')

        result = list(map(VertexMetadata.from_row, from_type_label_table.iterrows()))

        return result

    def add(self, db):
        query = """INSERT INTO %(type_label_table)s
        (eth, type, label, description) 
        VALUES (
            %(eth)s,
            %(type)s,
            %(label)s,
            %(description)s);"""
        result = db.bind.engine.execute(query, {
            'type_label_table': AsIs(VertexMetadata.__type_labels__),
            'eth': self.eth,
            'type': self.type,
            'label': self.label,
            'description': self.description
        })

        if self.account_type != None:
            query = """INSERT INTO %(account_table)s 
            (vertex, type) 
            VALUES (
                %(eth)s,
                %(account_type)s
            ) ON CONFLICT (vertex) DO UPDATE SET type = EXCLUDED.type;"""
            result = db.bind.engine.execute(query, {
                'account_table': AsIs(VertexMetadata.__account_type__),
                'eth': self.eth,
                'account_type': self.account_type
            })
    @staticmethod
    def from_row(row):
        result = VertexMetadata(eth=row[1]['eth'],
            type=row[1]['type'],
            label=row[1]['label'],
            account_type=int(row[1]['account_type']),
            description=row[1]['description'],
            id = row[1]['id'])
        return result

    @staticmethod
    def get_unique_by(db, page, by) -> List[str]:

        query = """SELECT DISTINCT %(column)s 
        FROM %(table_name)s
        LIMIT %(limit)s
        OFFSET %(offset)s;"""
        execute = db.bind.engine.execute(query, {
            'column': AsIs(by),
            'table_name': AsIs(VertexMetadata.__type_labels__),
            'limit': AsIs(AUTOCOMPLETE_TERMS_PER_PAGE),
            'offset': AsIs(AUTOCOMPLETE_TERMS_PER_PAGE * (page - 1))
        })
        frame = to_pd_frame(execute)
        return list(frame.values.flat)

    def __eq__(self, other):
        if not isinstance(other, VertexMetadata):
            return False
        return self.eth == other.eth and\
            self.type == other.type and\
            self.label == other.label and\
            self.account_type == other.account_type and\
            self.description == other.description
