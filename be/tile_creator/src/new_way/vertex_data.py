import cugraph
import numpy as np
import pandas as pd
from cugraph import Graph

from be.configuration import FA2_OPTIONS
from be.tile_creator.src.new_way.datasource import DataSource
from be.tile_creator.src.new_way.graph_data import GraphData
from be.tile_creator.src.new_way.gtm_args import GtmArgs


class VertexData():

    def __init__(self):
        # vertex_id, vertex_address, in_degree, out_degree,
        # graph_position, pixel_position
        # size, shape
        self.vertex_to_id = None
        self.vertex_to_degree = None
        self.positions = None
        self.positions_cudf = None
        self.positions_pixel = None

    def set_vertex_to_ids(self, datasource: DataSource):
        # get unique vertices (in case of eth network those are eth addresses)
        columnValues = datasource.data[["source", "target"]].values.ravel()
        uniqueValues = pd.unique(columnValues)

        # indices to vertices
        mapping = pd.DataFrame(uniqueValues) \
            .reset_index() \
            .rename(columns={0: "vertex"}) \
            .drop(columns=['index'])
        self.vertex_to_id = mapping

    def get_vertex_to_id(self):
        return self.vertex_to_id

    def set_degrees(self, cudf_graph):
        degrees = cudf_graph.degrees().to_pandas() \
            .sort_values(by=['vertex'])
        degrees = degrees.set_index('vertex')
        self.vertex_to_degree = degrees

    def get_degrees(self):
        return self.vertex_to_degree

    def set_positions(self, cudf_graph: Graph):

        layout = cugraph.layout.force_atlas2(cudf_graph, **FA2_OPTIONS)
        layout = layout \
            .sort_values(['vertex']) \
            .reset_index(drop=True) \
            .drop(columns=['vertex'])

        # Uncomment to spread the nodes on a square rather than a circle
        # layout = self._distribute_on_square_edges(layout)

        self.positions_cudf = layout

    def get_positions(self, cudf=False):
        if self.positions_cudf is None:
            return None
        if cudf:
            return self.positions_cudf
        return self.positions_cudf.to_pandas()

    def set_positions_pixel(self, gtm_args: GtmArgs, graph_data: GraphData):
        def convert_graph_coordinate_to_pixel(x, y,
                                              x_pixel, y_pixel,
                                              tile_size, min_coordinate, max_coordinate):
            """
            This function is specifically written to work with Rapids apply method: the apply method applies an operation
            on a GPU frame row by row.
            """
            graphSide = max_coordinate - min_coordinate
            for i, (sx, sy) in enumerate(zip(x, y)):
                scaling_factor = tile_size / graphSide
                x_pixel[i] = (sx + abs(min_coordinate)) * scaling_factor
                y_pixel[i] = (sy + abs(min_coordinate)) * scaling_factor

        merged = self.positions_cudf.apply_rows(convert_graph_coordinate_to_pixel,
                                                              incols=['x', 'y'],
                                                              outcols=dict(x_pixel=np.float64,
                                                                           y_pixel=np.float64),
                                                              kwargs={'tile_size': gtm_args.get_tile_size(),
                                                                      'min_coordinate': graph_data.get_vertex_bound().min,
                                                                      'max_coordinate': graph_data.get_vertex_bound().max})
        self.positions_pixel = merged.drop(columns=['x', 'y'])

    def get_positions_pixel(self):
        return self.positions_pixel

    def set_fake_positions(self, graph: GraphData):

        """
        This positions the fake vertices to ensure that the layout is a square
        :return:
        """

        if self.positions_cudf is None:
            raise Exception("Before setting the fake vertices positions you need to set the other vertices!")

        last_vertex_id, penultimum_vertex_id = self._get_last_2_vertices()

        def place_bottom_right(penultimum_vertex_id, graph: GraphData):
            self.positions_cudf.at[penultimum_vertex_id, 'y'] = graph.get_vertex_bound().max
            self.positions_cudf.at[penultimum_vertex_id, 'x'] = graph.get_vertex_bound().max

            self.positions_pixel.at[penultimum_vertex_id, 'x_pixel'] = graph.get_vertex_bound(pixel=True).max
            self.positions_pixel.at[penultimum_vertex_id, 'y_pixel'] = graph.get_vertex_bound(pixel=True).max

        def place_top_left(last_vertex_id, graph: GraphData):
            self.positions_cudf.at[last_vertex_id, 'x'] = graph.get_vertex_bound().min
            self.positions_cudf.at[last_vertex_id, 'y'] = graph.get_vertex_bound().min

            self.positions_pixel.at[last_vertex_id, 'x_pixel'] = graph.get_vertex_bound(pixel=True).min
            self.positions_pixel.at[last_vertex_id, 'y_pixel'] = graph.get_vertex_bound(pixel=True).min

        place_bottom_right(penultimum_vertex_id, graph)
        place_top_left(last_vertex_id, graph)

    def _get_last_2_vertices(self):
        last_vertex_id = self.positions_cudf.index.max()
        penultimum_vertex_id = last_vertex_id - 1
        return last_vertex_id, penultimum_vertex_id
