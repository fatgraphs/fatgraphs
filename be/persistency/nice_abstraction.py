from be.configuration import DB_USER_NAME, DB_PASSWORD, DB_URL, DB_NAME, METADATA_TABLE_NAME, VERTEX_TABLE_NAME, SRID
from be.persistency.db_connection import DbConnection
from be.persistency.implementation import Implementation, to_geopandas
from geoalchemy2 import Geometry
from sqlalchemy import String
import pandas as pd

"""
This class exposes the methods that are used to interact with the persistency layer, 
hiding the detail in the implementaiton.
"""


def to_pd_frame(raw_result):
    """
    :param raw_result: the object returned from executing a raw query with sqlAlchemy
    :return: a pandas frame where the column names are the DB column names and the rows are DB records
    """
    df = pd.DataFrame(raw_result.fetchall())
    df.columns = raw_result.keys()
    return df


class NiceAbstraction:
    '''
    Mehtods of here should return results that are easy to work with: either primitive types or pandas frames.
    '''
    def __init__(self, connection_string):
        self.connection = DbConnection(connection_string)
        self.impl = Implementation(self.connection)

    def create_metadata_table(self, graph_name, graph_metadata):
        table_name = METADATA_TABLE_NAME(graph_name)
        self.impl.save_frame_to_new_table(table_name, graph_metadata, {})

    def create_vertex_table(self, graph_name, layout, vertices_labels, id_to_eth):
        # TODO now only positions ae saved, in the future this table will contain ALL info related to vertices (degree, size, shape, label ...)

        # TODO refactor
        table_name = VERTEX_TABLE_NAME(graph_name)
        geopandas_frame = to_geopandas(layout.edge_ids_to_positions.to_pandas())

        s = geopandas_frame[['source_id', 'source_geo']].rename(columns={'source_id': 'id', 'source_geo': 'pos'})
        t = geopandas_frame[['target_id', 'target_geo']].rename(columns={'target_id': 'id', 'target_geo': 'pos'})
        geopandas_frame = pd.concat([s, t], axis=0).drop_duplicates()

        merge = geopandas_frame.merge(vertices_labels.vertices_labels[['vertex', 'label', 'type']], how='left',
                                      left_on='id', right_on='vertex')
        first = merge.groupby('id', as_index=False).first().drop(columns=['vertex'])

        id_to_eth = id_to_eth.rename(columns={'vertex': 'id', 'address': 'eth'})
        first_merge = first.merge(id_to_eth, on='id')
        all_in_one_frame = first_merge
        all_in_one_frame['size'] = layout.vertex_sizes
        column_types = {'pos': Geometry('POINT', srid=SRID)}
        self.impl.save_frame_to_new_table(table_name, all_in_one_frame, column_types)

    def create_edge_table(self):
        # TODO
        pass

    def get_closest_point(self, x, y, table):
        raw_result = self.impl.get_closest_point(x, y, table)
        df = to_pd_frame(raw_result)
        return df

    def get_graph_metadata(self, graph_name):
        raw_result = self.impl.get_graph_metadata(graph_name)
        df = to_pd_frame(raw_result)
        return df

    def get_labelled_vertices(self, graph_name):
        table_name = VERTEX_TABLE_NAME(graph_name)
        raw_result = self.impl.get_labelled_vertices(table_name)
        df = to_pd_frame(raw_result)
        return df

    def is_graph_in_db(self, graph_name):
        # TODO add edge_table and tiles_table and plot_table when they will exist
        tables_must_exist = [VERTEX_TABLE_NAME(graph_name),
                             METADATA_TABLE_NAME(graph_name)]
        return all(
            list(map(
                lambda table_name: self.connection.is_table_present(table_name),
                tables_must_exist
            ))
        )


# only one instance
singletonNiceAbstraction = NiceAbstraction(f'postgresql://{DB_USER_NAME}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}')
