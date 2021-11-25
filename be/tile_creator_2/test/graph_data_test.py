from .fixtures_edge import *  # noqa
from .fixtures_graph import *  # noqa
from .fixtures_vertex import *  # noqa
from .fixtures import *  # noqa

from be.tile_creator_2.edge_data import EdgeData
from be.tile_creator_2.graph_data import GraphData
from be.tile_creator_2.gtm_args import GtmArgs
from be.tile_creator_2.vertex_data import VertexData


class TestGraphData:


    def test_it_instanciate(self, graph_data):
        assert graph_data is not None

    def test_set_bounding_square(self, graph_data_bound: GraphData):
        assert graph_data_bound is not None
        assert graph_data_bound.graph_space_bound is not None
        assert graph_data_bound.graph_space_bound.max.x > graph_data_bound.graph_space_bound.min.x
        assert graph_data_bound.graph_space_bound.max.y > graph_data_bound.graph_space_bound.min.y

    def test_bounds_are_reasonable(self, graph_data_bound: GraphData, vertex_data_positions: VertexData):
        for (i, row) in vertex_data_positions.cudf_frame.to_pandas().iterrows():
            assert row['x'] <= graph_data_bound.graph_space_bound.max.x
            assert row['y'] <= graph_data_bound.graph_space_bound.max.y

            assert row['x'] >= graph_data_bound.graph_space_bound.min.x
            assert row['y'] >= graph_data_bound.graph_space_bound.min.y

    def test_set_bounding_square_pixel(self, graph_data_bound_pixel: GraphData):
        assert graph_data_bound_pixel is not None
        assert graph_data_bound_pixel.pixel_space_bound is not None
        assert graph_data_bound_pixel.pixel_space_bound.max.x > graph_data_bound_pixel.pixel_space_bound.min.x
        assert graph_data_bound_pixel.pixel_space_bound.max.y > graph_data_bound_pixel.pixel_space_bound.min.y

    def test_set_median_pixel_distance(self, graph_data_median: GraphData):
        assert graph_data_median.get_median_pixel_distance() is not None
        assert graph_data_median.get_median_pixel_distance() > 0

    def test_set_edge_count(self, graph_data_computed_properties: GraphData,
                            edge_data_lengths: EdgeData):
        assert graph_data_computed_properties.edge_count == len(edge_data_lengths.cudf_frame)

    def test_set_vertex_count(self, graph_data_computed_properties: GraphData,
                              vertex_data_positions_fake: VertexData):
        assert graph_data_computed_properties.vertex_count == len(vertex_data_positions_fake.cudf_frame)

    def test_set_graph_name(self, graph_data_computed_properties: GraphData, gtm_args: GtmArgs):
        assert gtm_args.get_name() == graph_data_computed_properties.graph_name
