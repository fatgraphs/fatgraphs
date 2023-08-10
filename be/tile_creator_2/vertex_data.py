import cudf
import cugraph
import numpy as np
from cugraph import Graph

from be.configuration import FA2_OPTIONS, CONFIGURATIONS
from be.tile_creator_2.datasource import DataSource
from be.tile_creator_2.graph_data import GraphData
from be.tile_creator_2.gtm_args import GtmArgs
from be.utils import shift_and_scale, timeit


class VertexData():

    def __init__(self):
        self.cudf_frame = None
        self.positions_pixel = None

    def set_vertex_to_ids(self, datasource: DataSource):
        # get unique vertices (in case of eth network those are eth addresses)
        uniqueValues = datasource.data["source"].append(datasource.data['target']).unique()

        # indices of frame to vertex id
        mapping = cudf.DataFrame(uniqueValues) \
            .reset_index() \
            .rename(columns={0: "vertex"})

        self.cudf_frame = mapping

    def set_degrees(self, cudf_graph):
        self.cudf_frame = self.cudf_frame.merge(
            cudf_graph.degrees()[['in_degree', 'out_degree']],
            left_index=True,
            right_index=True)

    def get_degrees(self):
        for column in ['in_degree', 'out_degree']:
            if column not in self.cudf_frame.columns:
                return None
        return self.cudf_frame[['in_degree', 'out_degree']]

    @timeit("Computing vertex positions")
    def set_positions(self, cudf_graph: Graph):
        """
        Uses fa2 to compute vertex positions.
        fa2 settings come from the configuration file
        :param cudf_graph:
        :return:
        """

        layout = cugraph.layout.force_atlas2(cudf_graph, **FA2_OPTIONS)
        self.cudf_frame = self.cudf_frame.merge(layout[['x', 'y']],
                                                left_index=True,
                                                right_index=True)

    def set_positions_pixel(self, gtm_args: GtmArgs, graph_data: GraphData):
        def convert_graph_coordinate_to_pixel(x, y,
                                              x_pixel, y_pixel,
                                              tile_size, min_coordinate, max_coordinate):
            """
            This function is specifically written to work with Rapids apply method: the apply method applies an operation
            on a GPU frame row by row.

            The graph "virtual" space is mapped to the pixel space based on the size of the
            tile
            """
            graphSide = max_coordinate - min_coordinate
            for i, (sx, sy) in enumerate(zip(x, y)):
                scaling_factor = tile_size / graphSide
                x_pixel[i] = (sx + abs(min_coordinate)) * scaling_factor
                y_pixel[i] = (sy + abs(min_coordinate)) * scaling_factor

        self.cudf_frame = self.cudf_frame.apply_rows(convert_graph_coordinate_to_pixel,
                                                     incols=['x', 'y'],
                                                     outcols=dict(x_pixel=np.float64,
                                                               y_pixel=np.float64),
                                                     kwargs={'tile_size': gtm_args.get_tile_size(),
                                                          'min_coordinate': graph_data.graph_space_bound.get_min_coord(),
                                                          'max_coordinate': graph_data.graph_space_bound.get_max_coord()})

    def set_corner_vertex_positions(self, graph: GraphData):

        """
        This positions the fake vertices to ensure that the layout is a square
        :return:
        """

        corenr_one, corner_two = self.get_corner_vertices_index()

        def place_bottom_right(penultimum_vertex_id, graph: GraphData):
            self.cudf_frame.at[penultimum_vertex_id, 'x'] = graph.graph_space_bound.get_max_coord()
            self.cudf_frame.at[penultimum_vertex_id, 'y'] = graph.graph_space_bound.get_max_coord()

            self.cudf_frame.at[penultimum_vertex_id, 'x_pixel'] = graph.pixel_space_bound.get_max_coord()
            self.cudf_frame.at[penultimum_vertex_id, 'y_pixel'] = graph.pixel_space_bound.get_max_coord()

        def place_top_left(last_vertex_id, graph: GraphData):
            self.cudf_frame.at[last_vertex_id, 'x'] = graph.graph_space_bound.get_min_coord()
            self.cudf_frame.at[last_vertex_id, 'y'] = graph.graph_space_bound.get_min_coord()

            self.cudf_frame.at[last_vertex_id, 'x_pixel'] = graph.pixel_space_bound.get_min_coord()
            self.cudf_frame.at[last_vertex_id, 'y_pixel'] = graph.pixel_space_bound.get_min_coord()

        place_top_left(corenr_one, graph)
        place_bottom_right(corner_two, graph)

    def get_corner_vertices_index(self):
        fake_one = self.cudf_frame.index[self.cudf_frame['vertex'] == CONFIGURATIONS['corner_vertices']['fake_vertex_1']].values[0]
        fake_two = self.cudf_frame.index[self.cudf_frame['vertex'] == CONFIGURATIONS['corner_vertices']['fake_vertex_2']].values[0]
        return fake_one, fake_two

    def set_sizes(self, graph_data: GraphData, gtm_args: GtmArgs):
        targetMedian = graph_data.median_pixel_distance * gtm_args.get_med_vertex_size()
        targetMax = graph_data.median_pixel_distance * gtm_args.get_max_vertex_size()
        v = shift_and_scale((self.cudf_frame['in_degree'] + self.cudf_frame['out_degree']).to_array(), targetMedian, targetMax)
        self.cudf_frame['size'] = v

    def get_sizes(self):
        return self.cudf_frame.sort_values(by="index")[['size']]

    def get_shapes(self):
        return self.cudf_frame.sort_values(by="index")['code']

    def get_positions(self):
        return self.cudf_frame.sort_values(by="index")[['x', 'y']]
