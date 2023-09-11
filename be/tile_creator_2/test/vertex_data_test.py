from be.configuration import CONFIGURATIONS, internal_id
from be.tile_creator_2.cudf_graph import CudfGraph
from be.tile_creator_2.edge_data import EdgeData
from be.tile_creator_2.graph_data import GraphData
from be.tile_creator_2.gtm_args import GtmArgs
from be.tile_creator_2.test.fixtures import get_vertices_from_file
from be.tile_creator_2.vertex_data import VertexData

from .fixtures_edge import *  # noqa
from .fixtures_graph import *  # noqa
from .fixtures_vertex import *  # noqa
from .fixtures import *  # noqa

class TestVertexData:

    def test_set_vertex_to_id(self, datasource, vertex_data: VertexData):
        assert vertex_data.cudf_frame is None or len(vertex_data.cudf_frame) == 0 or vertex_data.cudf_frame.empty
        vertex_data.set_vertex_to_ids(datasource)
        assert vertex_data.cudf_frame is not None and len(vertex_data.cudf_frame) > 0

    def test_all_vertices_are_present(self, vertex_data_id: VertexData):
        vertices_from_file = get_vertices_from_file()
        vertices_vertex_data = vertex_data_id.cudf_frame['vertex'].to_numpy()

        def assert_all_vertices_in_vertex_data_are_in_file_except_fake_vertices(vertices_from_file,
                                                                                vertices_vertex_data):
            assert all(
                v in vertices_from_file or v == CONFIGURATIONS['corner_vertices']['fake_vertex_1'] or\
                v == CONFIGURATIONS['corner_vertices']['fake_vertex_2']
                for
                v in vertices_vertex_data)

        def assert_all_vertices_in_file_are_in_vertex_data(vertices_from_file, vertices_vertex_data):
            assert all(v in vertices_vertex_data for v in vertices_from_file)

        assert_all_vertices_in_vertex_data_are_in_file_except_fake_vertices(vertices_from_file, vertices_vertex_data)
        assert_all_vertices_in_file_are_in_vertex_data(vertices_from_file, vertices_vertex_data)

    def test_set_degrees(self, vertex_data_id: VertexData, cudf_graph, edge_data_with_edges: EdgeData):
        assert vertex_data_id.get_degrees() is None
        vertex_data_id.set_degrees(cudf_graph.graph)
        assert vertex_data_id.get_degrees() is not None

        def assert_each_vertex_has_a_degree(cudf_graph: CudfGraph, vertex_data_id):
            assert len(vertex_data_id.get_degrees()) == cudf_graph.get_vertexcount()

        assert_each_vertex_has_a_degree(cudf_graph, vertex_data_id)
        for (index, row) in vertex_data_id.cudf_frame.to_pandas().iterrows():
            calculated_degree = (edge_data_with_edges.cudf_frame[
                                     internal_id("source")] == index).sum() + (
                                        edge_data_with_edges.cudf_frame[
                                            internal_id("target")] == index).sum()

            set_degree = vertex_data_id.get_degrees().loc[index]['in_degree'] + \
                         vertex_data_id.get_degrees().loc[index]['out_degree']

            assert set_degree == calculated_degree

    def test_set_position(self, vertex_data_degrees: VertexData, cudf_graph):
        assert 'x' not in vertex_data_degrees.cudf_frame.columns, "vertex_data should NOT contain positions at this stage"
        assert 'y' not in vertex_data_degrees.cudf_frame.columns, "vertex_data should NOT contain positions at this stage"

        vertex_data_degrees.set_positions(cudf_graph.graph)

        assert 'x' in vertex_data_degrees.cudf_frame.to_pandas().columns, "vertex positions should have a x column"
        assert 'y' in vertex_data_degrees.cudf_frame.to_pandas().columns, "vertex positions should have a y column"
        assert len(vertex_data_degrees.cudf_frame) == cudf_graph.get_vertexcount(), "there should be as many " \
                                                                                         "positions as there are " \
                                                                                         "vertices "

    def test_get_corber_vertices(self, vertex_data_positions: VertexData):
        # TODO add check for amount with right vertex data obj
        corner_vertex_1, corner_vertex_2 = vertex_data_positions.get_corner_vertices_index()
        assert vertex_data_positions.cudf_frame['in_degree'][corner_vertex_1] \
               == vertex_data_positions.cudf_frame['out_degree'][corner_vertex_1] == 1

        assert vertex_data_positions.cudf_frame['in_degree'][corner_vertex_2] \
               == vertex_data_positions.cudf_frame['out_degree'][corner_vertex_2] == 1

    def test_set_fake_positions(self, vertex_data_positions_pixel: VertexData, graph_data_bound_pixel: GraphData):

        def assert_corner_vertices_are_positioned_at_corners(corner_1, corner_2,
                                                             vertex_data_positions_pixel):
            assert vertex_data_positions_pixel.cudf_frame['x'][corner_1] \
                   == vertex_data_positions_pixel.cudf_frame['y'][corner_1]

            assert vertex_data_positions_pixel.cudf_frame['x'][corner_2] \
                   == vertex_data_positions_pixel.cudf_frame['y'][corner_2]

        def assert_corner_vertices_position_is_random(corner_1, corner_2,
                                                      vertex_data_positions_pixel):
            assert vertex_data_positions_pixel.cudf_frame['x'][corner_1] \
            != vertex_data_positions_pixel.cudf_frame['y'][corner_1]

            assert vertex_data_positions_pixel.cudf_frame['x'][corner_2] \
            != vertex_data_positions_pixel.cudf_frame['y'][corner_2]

        last_vertex, penultimum_vertex = vertex_data_positions_pixel.get_corner_vertices_index()

        assert_corner_vertices_position_is_random(last_vertex, penultimum_vertex, vertex_data_positions_pixel)

        assert graph_data_bound_pixel.graph_space_bound is not None
        assert graph_data_bound_pixel.pixel_space_bound is not None

        vertex_data_positions_pixel.set_corner_vertex_positions(graph_data_bound_pixel)

        assert_corner_vertices_are_positioned_at_corners(last_vertex, penultimum_vertex, vertex_data_positions_pixel)

    def test_set_vertex_size(self, vertex_data_size: VertexData,
                             gtm_args: GtmArgs,
                             graph_data_computed_properties: GraphData
                             ):
        for (i, row) in vertex_data_size.cudf_frame.to_pandas().iterrows():
            assert row['size'] > 0
            assert row['size'] <= gtm_args.get_max_vertex_size() * graph_data_computed_properties.get_median_pixel_distance()