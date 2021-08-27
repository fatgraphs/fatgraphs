from be.configuration import CONFIGURATIONS, internal_id
from be.tile_creator.src.new_way.cudf_graph import CudfGraph
from be.tile_creator.src.new_way.test.fixtures_vertex import *
from be.tile_creator.src.new_way.test.fixtures import *
from be.tile_creator.src.new_way.test.fixtures_graph import *
from be.tile_creator.src.new_way.test.fixtures_edge import *
from be.tile_creator.src.new_way.vertex_data import VertexData


class TestVertexData:

    def test_vertex_to_id_is_not_none(self, datasource, vertex_data: VertexData):
        assert vertex_data.vertex_to_id is None or len(vertex_data.vertex_to_id) == 0
        vertex_data.set_vertex_to_ids(datasource)
        assert vertex_data.vertex_to_id is not None and len(vertex_data.vertex_to_id) > 0

    def test_all_vertices_are_present(self, vertex_data_id: VertexData):
        vertices_from_file = get_vertices_from_file()
        vertices_vertex_data = vertex_data_id.get_vertex_to_id()['vertex'].values

        def assert_all_vertices_in_vertex_data_are_in_file_except_fake_vertices(vertices_from_file,
                                                                                vertices_vertex_data):
            assert all(
                v in vertices_from_file or v == CONFIGURATIONS['fake_vertex_1'] or v == CONFIGURATIONS['fake_vertex_2']
                for
                v in vertices_vertex_data)

        def assert_all_vertices_in_file_are_in_vertex_data(vertices_from_file, vertices_vertex_data):
            assert all(v in vertices_vertex_data for v in vertices_from_file)

        assert_all_vertices_in_vertex_data_are_in_file_except_fake_vertices(vertices_from_file, vertices_vertex_data)
        assert_all_vertices_in_file_are_in_vertex_data(vertices_from_file, vertices_vertex_data)

    def test_set_degrees(self, vertex_data_id: VertexData, cudf_graph, edge_data_with_edges: EdgeData):
        assert vertex_data_id.get_degrees() is None
        vertex_data_id.set_degrees(cudf_graph.get_graph())
        assert vertex_data_id.get_degrees() is not None

        def assert_each_vertex_has_a_degree(cudf_graph: CudfGraph, vertex_data_id):
            assert len(vertex_data_id.get_degrees()) == cudf_graph.get_vertexcount()

        assert_each_vertex_has_a_degree(cudf_graph, vertex_data_id)
        for (index, row) in vertex_data_id.get_vertex_to_id().iterrows():
            calculated_degree = (edge_data_with_edges.get_source_target_amount()[
                                     internal_id("source")] == index).sum() + (
                                        edge_data_with_edges.get_source_target_amount()[
                                            internal_id("target")] == index).sum()

            set_degree = vertex_data_id.get_degrees().loc[index]['in_degree'] + \
                         vertex_data_id.get_degrees().loc[index]['out_degree']

            assert set_degree == calculated_degree

    def test_set_position(self, vertex_data_degrees: VertexData, cudf_graph):
        assert vertex_data_degrees.get_positions() is None, "vertex_data should NOT contain positions at this stage"
        vertex_data_degrees.set_positions(cudf_graph.get_graph())
        assert vertex_data_degrees.get_positions() is not None, "vertex_data SHOULD contain positions at this stage"
        assert 'x' in vertex_data_degrees.get_positions().columns, "vertex positions should have a x column"
        assert 'y' in vertex_data_degrees.get_positions().columns, "vertex positions should have a y column"
        assert len(vertex_data_degrees.get_positions()) == cudf_graph.get_vertexcount(), "there should be as many " \
                                                                                         "positions as there are " \
                                                                                         "vertices "

    def test_get_last_two_vertices(self, vertex_data_positions: VertexData):
        last, penultimum = vertex_data_positions._get_last_2_vertices()
        assert last == len(vertex_data_positions.get_positions()) - 1
        assert last == penultimum + 1

    def test_set_fake_positions(self, vertex_data_positions_pixel: VertexData, graph_data_bound_pixel: GraphData):
        last_vertex, penultimum_vertex = vertex_data_positions_pixel._get_last_2_vertices()

        for list_coords in [vertex_data_positions_pixel.get_positions(),
                            vertex_data_positions_pixel.get_positions(cudf=True),
                            vertex_data_positions_pixel.get_positions_pixel()]:
            for index in [last_vertex, penultimum_vertex]:
                x = 'x' if 'x' in list_coords.columns else 'x_pixel'
                y = 'y' if 'y' in list_coords.columns else 'y_pixel'
                assert list_coords.loc[index][x] != list_coords.loc[index][y]

        assert graph_data_bound_pixel.get_vertex_bound() is not None
        assert graph_data_bound_pixel.get_vertex_bound(pixel=True) is not None

        vertex_data_positions_pixel.set_fake_positions(graph_data_bound_pixel)

        for list_coords in [vertex_data_positions_pixel.get_positions(),
                            vertex_data_positions_pixel.get_positions(cudf=True),
                            vertex_data_positions_pixel.get_positions_pixel()]:
            for index in [last_vertex, penultimum_vertex]:
                x = 'x' if 'x' in list_coords.columns else 'x_pixel'
                y = 'y' if 'y' in list_coords.columns else 'y_pixel'
                assert list_coords.loc[index][x] == pytest.approx(list_coords.loc[index][y])
