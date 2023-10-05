import pandas as pd
from psycopg2._psycopg import AsIs

from be.server import engine
from be.server.utils import to_pd_frame
from sqlalchemy.sql import text


class VertexMetadata:
    """
    Vertex (e.g. eth address) not usd as primary key as there could be diplicates
    """

    __type_labels__ = "tg_vertex_metadata"
    __account_type__ = "tg_account_type"

    def __init__(self,
        vertex: str,
        type: str = None,
        label: str = None,
        account_type: int = None,
        description: str = None,
        id: int = None,):

        self.id = id
        self.vertex = vertex
        self.type = type
        self.label = label
        self.account_type = account_type
        self.description = description


    @staticmethod
    def merge_for_account_types(graph_vertex_table_name: str):
        query = text(
            """
            SELECT * FROM :graph_vertex_table_name 
            INNER JOIN :tg_account_type 
            ON :tg_account_type.vertex = :graph_vertex_table_name.vertex
            """
        )

        with engine.connect() as conn:

            raw_result = conn.execute(query, {
                'graph_vertex_table_name': AsIs(graph_vertex_table_name),
                'tg_account_type': 'tg_account_type'
                })


    @staticmethod
    def filter_by(db: object, vertex=None, type=None, label=None):
        query = """SELECT * FROM  :type_label_table """

        substitution = {'type_label_table': AsIs(VertexMetadata.__type_labels__)}

        if vertex != None:
            query = query + """WHERE vertex = :vertex """
            substitution['vertex'] = vertex

        if type != None:
            query = query + """WHERE type = :type """
            substitution['type'] = type

        if label != None:
            query = query + """WHERE label = :label """
            substitution['label'] = label

        query = query + ';'
        query = text(query)

        with engine.connect() as conn:

            result = conn.execute(query, substitution)

            from_type_label_table = to_pd_frame(result)
            if from_type_label_table.empty:
                return []
            # so it doesn't break if account_types is empty
            account_types = pd.DataFrame(columns=["vertex"])
            for vertex_ in list(set(from_type_label_table['vertex'].values)):
                query = text(
                    """
                    SELECT * FROM :account_table WHERE :account_table.vertex = :vertex
                    """
                )

                result = conn.execute(query, {
                    'account_table': AsIs(VertexMetadata.__account_type__),
                    'vertex': vertex_})
                frame = to_pd_frame(result)
                account_types = account_types.append(frame)

            accounts = account_types.rename(
                columns={'type': 'account_type'}
            )

            from_type_label_table = from_type_label_table.merge(
                accounts, 
                left_on='vertex', right_on='vertex'
            )

            result = list(map(VertexMetadata.from_row, from_type_label_table.iterrows()))

            return result

    def add(self, db):
        query = text(
            """
            INSERT INTO :type_label_table
            (vertex, type, label, description) 
            VALUES (
                :vertex,
                :type,
                :label,
                :description);
            """
        )
        
        with engine.connect() as conn:
            result = conn.execute(
                query, 
                {
                'type_label_table': AsIs(VertexMetadata.__type_labels__),
                'vertex': self.vertex,
                'type': self.type,
                'label': self.label,
                'description': self.description
                }
            )

            if self.account_type != None:
                query = text(
                    """
                    INSERT INTO :account_table 
                    (vertex, type) 
                    VALUES (
                        :vertex,
                        :account_type
                    ) ON CONFLICT (vertex) DO UPDATE SET type = EXCLUDED.type;
                    """
                )

                with engine.connect() as conn:
                    result = conn.execute(
                        query, 
                        {
                            'account_table': AsIs(VertexMetadata.__account_type__),
                            'vertex': self.vertex,
                            'account_type': self.account_type
                        }
                    )
                
    @staticmethod
    def delete(vertex, typee, value, db):
        query = text(
            """
            UPDATE :type_label_table 
            SET :type_or_label = ''
            WHERE vertex = :vertex AND :type_or_label = :value; 
            """
        )

        with engine.connect() as conn:
            result = conn.execute(
                query, 
                {
                    'type_label_table': AsIs(VertexMetadata.__type_labels__),
                    'type_or_label': AsIs(typee),
                    'vertex': vertex,
                    'value': value
                }
            )
            return result

    @staticmethod
    def from_row(row):
        result = VertexMetadata(vertex=row[1]['vertex'],
            type=row[1]['type'],
            label=row[1]['label'],
            account_type=int(row[1]['account_type']),
            description=row[1]['description'],
            id = row[1]['id'])
        return result

    def __eq__(self, other):
        if not isinstance(other, VertexMetadata):
            return False
        return self.vertex == other.vertex and\
            self.type == other.type and\
            self.label == other.label and\
            self.account_type == other.account_type and\
            self.description == other.description
