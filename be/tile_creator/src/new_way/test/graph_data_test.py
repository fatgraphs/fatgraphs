from be.tile_creator.src.new_way.test.fixtures_vertex import *
from be.tile_creator.src.new_way.test.vertex_data_test import *

class TestGraphData:


    def test_it_instanciate(self, graph_data):
        assert graph_data is not None

    def test_set_bounding_square(self, graph_data_bound: GraphData):
        assert graph_data_bound is not None
        assert graph_data_bound.get_vertex_bound() is not None
        assert graph_data_bound.get_vertex_bound().max > graph_data_bound.get_vertex_bound().min

    def test_bounds_are_reasonable(self, graph_data_bound: GraphData, vertex_data_positions: VertexData):
        for (i, row) in vertex_data_positions.get_positions().iterrows():
            assert row['x'] <= graph_data_bound.get_vertex_bound().max
            assert row['y'] <= graph_data_bound.get_vertex_bound().max

            assert row['y'] >= graph_data_bound.get_vertex_bound().min
            assert row['x'] >= graph_data_bound.get_vertex_bound().min

    def test_set_bounding_square_pixel(self, graph_data_bound_pixel: GraphData):
        assert graph_data_bound_pixel is not None
        assert graph_data_bound_pixel.get_vertex_bound(pixel=True) is not None
        assert graph_data_bound_pixel.get_vertex_bound(pixel=True).max > graph_data_bound_pixel.get_vertex_bound(pixel=True).min

    def test_set_median_pixel_distance(self, graph_data_median: GraphData):
        assert graph_data_median.get_median_pixel_distance() is not None
        assert graph_data_median.get_median_pixel_distance() > 0
