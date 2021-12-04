import numpy as np

from be.server.vertex_metadata.service import VertexMetadataService
from be.tile_creator_2.vertex_data import VertexData
import cudf

from be.utils import timeit


class ShapeGenerator:

    def __init__(self, db, graph_id: int):
        self.db = db
        self.graph_id = graph_id

    @timeit("Generating vertex shapes")
    def augment_vertex_data(self, og_vertex_data: VertexData):
        # convert to pandas as it's more flexible then cudf
        vertex_data = og_vertex_data.cudf_frame[['vertex']]

        vertex_data = self.augment_with_acount(vertex_data)

        vertex_data = self.assume_vertex_with_associated_acount_is_unlabled(vertex_data)

        vertex_data = self.mark_vertex_without_acount_fake(vertex_data)

        vertex_data = self.augment_vertex_data_w_labels(vertex_data)

        ShapeGenerator.mark_labelled(vertex_data)

        vertex_frame = ShapeGenerator.reduce(vertex_data)
        vertex_frame = ShapeGenerator.merge(vertex_frame)
        vertex_frame = ShapeGenerator.map(vertex_frame)

        og_vertex_data.cudf_frame = og_vertex_data.cudf_frame.merge(vertex_frame[['vertex', 'code']], how='left')

        return og_vertex_data

    @staticmethod
    def map(nice_frame):
        int_to_icon = {
            '0': 'inactive_fake',
            '1': 'eoa_unlabelled',
            '2': 'eoa_labelled',
            '3': 'ca_unlabelled',
            '4': 'ca_labelled'
        }
        # notice that pandas.replace leaves untouched values not present in the dict key
        nice_frame['code'] = nice_frame['code'].replace(int_to_icon)
        return nice_frame

    @staticmethod
    def merge(nice_frame):
        # after this the icon column stores a union type: a code or a png file name if the vertex had a custom icon
        nice_frame['icon'] = nice_frame['icon'].replace({
            None: "None"
        })
        nice_frame['code'] = nice_frame['code'].astype({'code': 'string'})
        nice_frame['code'] = np.where(nice_frame['icon'].to_array() == "None", nice_frame['code'].to_array(), nice_frame['icon'].to_array())
        return nice_frame

    @staticmethod
    def reduce(vertex_frame):
        # Because the same vertex may appear many times in the labels, vertex data can have duplicates
        # e.g. vertex1 is associated both with a labelled and a unlabelled record
        # but if we had reason to say it was labelled than that must be the truth.
        # Because of the way we have defined codes taking the max deals with this situation.

        # Notice that if a vertex appears as both fake_inactive (code 0) and as ca_labelled (code 4)
        # it will become ca_labelled.

        # A more refined logic for choosing the shape_code for a vertex having many types/labels/accounts association
        # will go here
        vertex_frame = vertex_frame.groupby(['vertex'], sort=False) \
            .agg({'code': 'max',
                  'icon': ShapeGenerator.longestFilename}) \
            .reset_index()

        return vertex_frame

    def augment_vertex_data_w_labels(self, vertex_data):
        def fetch_vertex_labels_mapping():
            return VertexMetadataService.merge_graph_vertices_with_metadata(self.graph_id, self.db)

        metadata = fetch_vertex_labels_mapping()
        metadata = cudf.DataFrame.from_pandas(metadata)
        metadata = metadata[['vertex', 'type', 'label', 'icon']]
        result = vertex_data.merge(metadata, left_on='vertex', right_on='vertex', how='left')
        # after the merge some rows will have type = Nan
        # rows where the condition if FALSE are substituted with 0
        # result['type'] = result['type'].where(result['type'].notna(), 0)
        result['type'] = np.where(result['type'].to_array() == None, '0', result['type'].to_array())
        return result

    @staticmethod
    def assume_vertex_with_associated_acount_is_unlabled(vertex_data_with_acount):
        # if a vertex is found in the vertex list it means it's either eoa or ca
        # but is it labelled or unlabeled? For now we assume unlabelled

        EO_CODE_IN_RAW_DATA = 0
        CA_CODE_IN_RAW_DATA = 1

        vertex_data_with_acount['code'] = vertex_data_with_acount['code'].replace(
            {
                EO_CODE_IN_RAW_DATA: 1,
                CA_CODE_IN_RAW_DATA: 3
            })
        return vertex_data_with_acount

    def augment_with_acount(self, vertex_data):
        def fetch_vertex_acount_mapping():
            account_types = VertexMetadataService.merge_graph_vertices_with_account_type(self.db, self.graph_id)
            account_types = account_types.rename(columns={'type': 'code'})
            return account_types

        account_types = fetch_vertex_acount_mapping()
        account_types = cudf.DataFrame.from_pandas(account_types)
        result = vertex_data.merge(account_types, how='left')
        return result

    @staticmethod
    def mark_vertex_without_acount_fake(result):
        return result.fillna(0)

    @staticmethod
    def mark_labelled(vertex_data):
        # increment by 1 where type is not 0 (i.e. type == 'exchange')
        # this works becaue the ic
        vertex_data['code'] = vertex_data['code'] + np.where(vertex_data['type'].to_array() == '0', 0, 1)

    @staticmethod
    def longestFilename(s):
        # If the same vertices has two custom icons defined,
        # arbitrarily pick the longest string
        return s.max()
