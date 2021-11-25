import numpy as np
import pandas as pd

from be.configuration import CONFIGURATIONS, internal_id, external_id
from be.tile_creator_2.datasource import DataSource
from be.tile_creator_2.graph_data import GraphData
from be.tile_creator_2.gtm_args import GtmArgs
from be.tile_creator_2.vertex_data import VertexData
from be.utils import shift_and_scale


class EdgeData():

    def __init__(self):
        self.cudf_frame = None
        self.transparencies = None

    def set_cudf_frame(self, datasource: DataSource, vertex_data: VertexData):
        # add index as a new column
        # vertex_id_mapping[CONFIGURATIONS['vertex_internal_id']] = vertex_id_mapping.index

        # TODO refactor
        vertex_to_id_source = vertex_data.cudf_frame \
            .rename(columns={CONFIGURATIONS['vertex_external_id']: "source"})
        source_target_amount = datasource.data.merge(vertex_to_id_source)
        source_target_amount = source_target_amount.rename(columns={'source': external_id("source")})
        source_target_amount = source_target_amount.rename(columns={'index': internal_id("source")})

        vertex_to_id_target = vertex_data.cudf_frame \
            .rename(columns={CONFIGURATIONS['vertex_external_id']: "target"})
        source_target_amount = source_target_amount.merge(vertex_to_id_target)
        source_target_amount = source_target_amount.rename(columns={'target': external_id("target")})
        source_target_amount = source_target_amount.rename(columns={'index': internal_id("target")})

        source_target_amount = source_target_amount.sort_values([internal_id("source"),
                                                                 internal_id("target")])
        source_target_amount = source_target_amount.reset_index(drop=True)
        self.cudf_frame = source_target_amount

    # def populate_source_target_amount_cudf(self):
    #     self.source_target_amount_cudf = cudf.DataFrame.from_pandas(self.source_target_amount)

    def set_ids_to_position(self, vertex_data):
        src = self._join_positions('source', vertex_data.cudf_frame, {'x': 'source_x',
                                                                      'y': 'source_y'})
        trg = self._join_positions('target', vertex_data.cudf_frame, {'x': 'target_x',
                                                                      'y': 'target_y'})
        merged = trg.merge(src) \
            .sort_values(by=[internal_id('source'), internal_id('target')]) \
            .reset_index(drop=True)

        self.cudf_frame = self.cudf_frame.reset_index() \
            .merge(merged, how="left") \
            .set_index('index') \
            .sort_index()


    def set_ids_to_pixel_position(self, vertex_data):
        src = self._join_positions('source', vertex_data.cudf_frame, {'x_pixel': 'source_x_pixel',
                                                              'y_pixel': 'source_y_pixel'})
        trg = self._join_positions('target', vertex_data.cudf_frame, {'x_pixel': 'target_x_pixel',
                                                              'y_pixel': 'target_y_pixel'})
        merged = trg.merge(src) \
            .sort_values(by=[internal_id('source'), internal_id('target')]) \
            .reset_index(drop=True)

        self.cudf_frame = self.cudf_frame.reset_index() \
            .merge(merged, how="left") \
            .set_index('index') \
            .sort_index()

    def get_ids_to_pos(self):
        position_columns = ['target_x',
                            'target_y',
                            'source_x',
                            'source_y']

        for col in position_columns:
            if col not in self.cudf_frame.columns:
                return None

        return self.cudf_frame[[internal_id('source'),  internal_id('target'),
                                external_id('source'), external_id('target'),
                               *position_columns]]

    def get_ids_to_pos_pixel(self):
        position_columns = ['target_x_pixel',
                            'target_y_pixel',
                            'source_x_pixel',
                            'source_y_pixel']

        for col in position_columns:
            if col not in self.cudf_frame.columns:
                return None

        return self.cudf_frame[[internal_id('source'), internal_id('target'),
                                external_id('source'), external_id('target'),
                                *position_columns]]

    def _join_positions(self, source_or_target, positions_to_join, column_renames):
        positions_to_join = positions_to_join.rename(columns=column_renames)
        graphPositions = self.cudf_frame.merge(
            positions_to_join[list(column_renames.values())],
            left_on=[internal_id(source_or_target)],
            right_index=True)
        return graphPositions

    def set_thickness(self, graph_data: GraphData, gtm_args: GtmArgs):

        def set_corner_vertex_self_edge_zero(self):
            index_1 = self.cudf_frame[
                self.cudf_frame['source_vertex'] == CONFIGURATIONS['corner_vertices']['fake_vertex_1']].index
            index_2 = self.cudf_frame[
                self.cudf_frame['source_vertex'] == CONFIGURATIONS['corner_vertices']['fake_vertex_2']].index
            self.cudf_frame.at[index_1, 'thickness'] = 0
            self.cudf_frame.at[index_2, 'thickness'] = 0

        def calculateEdgesThickness(amounts, medEdgeThickness, maxEdgeThickness):
            target_median = graph_data.get_median_pixel_distance() * medEdgeThickness
            target_max = graph_data.get_median_pixel_distance() * maxEdgeThickness
            return shift_and_scale(amounts, target_median, target_max, 1.0)

        logAmounts = np.log10(
            self.cudf_frame['amount'].values + 10)  # amounts can be huge numbers, reduce the range

        thickness_array = calculateEdgesThickness(logAmounts,
                                                  gtm_args.get_median_edge_thickness(),
                                                  gtm_args.get_max_edge_thickness())

        thickness = pd.DataFrame(thickness_array) \
            .rename(columns={0: 'thickness'})

        self.cudf_frame['thickness'] = thickness['thickness']
        set_corner_vertex_self_edge_zero(self)

    def get_thickness(self):
        return self.cudf_frame['thickness']

    def set_lengths(self):
        distances = ((self.cudf_frame['source_x'] - self.cudf_frame['target_x']) ** 2 + (
                self.cudf_frame['source_y'] - self.cudf_frame['target_y']) ** 2) ** 0.5
        self.cudf_frame['lengths'] = distances

    def get_lengths(self):
        return self.cudf_frame['lengths']

    def get_transparencies(self):
        return self.transparencies