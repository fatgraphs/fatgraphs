import cudf
import numpy as np
import pandas as pd

from be.configuration import CONFIGURATIONS, internal_id, external_id
from be.tile_creator.src.new_way.datasource import DataSource
from be.tile_creator.src.new_way.graph_data import GraphData
from be.tile_creator.src.new_way.gtm_args import GtmArgs
from be.utils import shift_and_scale


class EdgeData():

    def __init__(self):
        # vertex_id, vertex_address, in_degree, out_degree,
        # graph_position, pixel_position
        # size, shape
        # self.source_target_amount = None  # prev known as: edgeIdToAmount
        self.source_target_amount_cudf = None
        self.ids_to_pos = None
        self.ids_to_pos_pixel = None
        self.thickness = None

    def set_source_target_amount(self, datasource: DataSource, og_vertex_to_id):
        # add index as a new column
        og_vertex_to_id[CONFIGURATIONS['vertex_internal_id']] = og_vertex_to_id.index

        # TODO refactor
        vertex_to_id_source = og_vertex_to_id.rename(columns={CONFIGURATIONS['vertex_external_id']: "source"})
        source_target_amount = datasource.data.merge(vertex_to_id_source)
        source_target_amount = source_target_amount.rename(columns={'source': external_id("source")})
        source_target_amount = source_target_amount.rename(columns={'index': internal_id("source")})

        vertex_to_id_target = og_vertex_to_id.rename(columns={CONFIGURATIONS['vertex_external_id']: "target"})
        source_target_amount = source_target_amount.merge(vertex_to_id_target)
        source_target_amount = source_target_amount.rename(columns={'target': external_id("target")})
        source_target_amount = source_target_amount.rename(columns={'index': internal_id("target")})

        source_target_amount = source_target_amount.sort_values([internal_id("source"),
                                                                 internal_id("target")])
        source_target_amount = source_target_amount.reset_index(drop=True)
        self.source_target_amount_cudf = cudf.DataFrame.from_pandas(source_target_amount)

    # def populate_source_target_amount_cudf(self):
    #     self.source_target_amount_cudf = cudf.DataFrame.from_pandas(self.source_target_amount)

    def get_source_target_amount(self):
        return self.source_target_amount_cudf

    def set_ids_to_position(self, cudf_positions):
        src = self._join_positions('source', cudf_positions, {'x': 'source_x',
                                                              'y': 'source_y'})
        trg = self._join_positions('target', cudf_positions, {'x': 'target_x',
                                                              'y': 'target_y'})
        merged = trg.merge(src) \
            .sort_values(by=[internal_id('source'), internal_id('target')]) \
            .reset_index(drop=True)

        self.ids_to_pos = merged

    def set_ids_to_pixel_position(self, cudf_positions):
        src = self._join_positions('source', cudf_positions, {'x_pixel': 'source_x_pixel',
                                                              'y_pixel': 'source_y_pixel'})
        trg = self._join_positions('target', cudf_positions, {'x_pixel': 'target_x_pixel',
                                                              'y_pixel': 'target_y_pixel'})
        merged = trg.merge(src) \
            .sort_values(by=[internal_id('source'), internal_id('target')]) \
            .reset_index(drop=True)

        self.ids_to_pos_pixel = merged

    def get_ids_to_pos(self, pixel=False):
        if pixel:
            return self.ids_to_pos_pixel
        return self.ids_to_pos

    def _join_positions(self, source_or_target, positions_to_join, column_renames):
        positions_to_join = positions_to_join.rename(columns=column_renames)
        graphPositions = self.source_target_amount_cudf \
            .merge(positions_to_join, left_on=[internal_id(source_or_target)], right_index=True)
        return graphPositions

    def set_thickness(self, graph_data: GraphData, gtm_args: GtmArgs):
        def calculateEdgesThickness(amounts, medEdgeThickness, maxEdgeThickness):
            target_median = graph_data.get_median_pixel_distance() * medEdgeThickness
            target_max = graph_data.get_median_pixel_distance() * maxEdgeThickness
            return shift_and_scale(amounts, target_median, target_max, 1.0)

        logAmounts = np.log10(
            self.source_target_amount_cudf['amount'].values + 10)  # amounts can be huge numbers, reduce the range

        thickness_array = calculateEdgesThickness(logAmounts,
                                                  gtm_args.get_median_edge_thickness(),
                                                  gtm_args.get_max_edge_thickness())

        thickness = pd.DataFrame(thickness_array) \
            .rename(columns={0: 'thickness'})

        thickness.at[len(thickness_array) - 1, 'thickness'] = 0.0
        thickness.at[len(thickness_array) - 2, 'thickness'] = 0.0

        self.thickness = thickness

    def get_thickness(self):
        return self.thickness
