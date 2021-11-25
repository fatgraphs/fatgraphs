from .fixtures_edge import *  # noqa
from .fixtures_graph import *  # noqa
from .fixtures_vertex import *  # noqa
from .fixtures import *  # noqa

from be.tile_creator_2.graph_data import GraphData
from be.tile_creator_2.edge_data import EdgeData
from be.tile_creator_2.vertex_data import VertexData
from be.configuration import internal_id, external_id, CONFIGURATIONS
from be.tile_creator_2.datasource import DataSource
from be.utils import calculate_diagonal_square_of_side


class TestEdgeData:

    def test_set_source_target_amount(self, edge_data_with_edges: EdgeData, datasource: DataSource):
        assert edge_data_with_edges.cudf_frame is not None
        assert len(datasource.get_data()) == len(edge_data_with_edges.cudf_frame)
        for e in [external_id('source'), external_id('target'), 'amount']:
            assert e in edge_data_with_edges.cudf_frame.columns

    def test_ids_to_positions(self, edge_data_with_edges: EdgeData, vertex_data_positions: VertexData):
        assert edge_data_with_edges.get_ids_to_pos() is None, "at this stage edge data should NOT contain the " \
                                                              "ids to position mappings "
        edge_data_with_edges.set_ids_to_position(vertex_data_positions)

        assert edge_data_with_edges.get_ids_to_pos() is not None, "at this stage edge data SHOULD contain the " \
                                                                  "ids to position mappings "

        assert len(edge_data_with_edges.get_ids_to_pos()) == len(edge_data_with_edges.cudf_frame)

        assert internal_id("source") in edge_data_with_edges.get_ids_to_pos().columns
        assert internal_id("target") in edge_data_with_edges.get_ids_to_pos().columns
        assert external_id("source") in edge_data_with_edges.get_ids_to_pos().columns
        assert external_id("target") in edge_data_with_edges.get_ids_to_pos().columns

        assert "source_x" in edge_data_with_edges.get_ids_to_pos().columns
        assert "target_x" in edge_data_with_edges.get_ids_to_pos().columns
        assert "source_y" in edge_data_with_edges.get_ids_to_pos().columns
        assert "target_y" in edge_data_with_edges.get_ids_to_pos().columns

    def test_id_to_pixel_position(self, edge_data_positions_pixel: EdgeData):
        assert edge_data_positions_pixel.get_ids_to_pos_pixel() is not None
        assert len(edge_data_positions_pixel.get_ids_to_pos_pixel()) == \
               len(edge_data_positions_pixel.get_ids_to_pos())

        assert internal_id("source") in edge_data_positions_pixel.get_ids_to_pos_pixel().columns
        assert internal_id("target") in edge_data_positions_pixel.get_ids_to_pos_pixel().columns
        assert external_id("source") in edge_data_positions_pixel.get_ids_to_pos_pixel().columns
        assert external_id("target") in edge_data_positions_pixel.get_ids_to_pos_pixel().columns

        assert "source_x_pixel" in edge_data_positions_pixel.get_ids_to_pos_pixel().columns
        assert "target_x_pixel" in edge_data_positions_pixel.get_ids_to_pos_pixel().columns
        assert "source_y_pixel" in edge_data_positions_pixel.get_ids_to_pos_pixel().columns
        assert "target_y_pixel" in edge_data_positions_pixel.get_ids_to_pos_pixel().columns

    def test_set_thickness(self, edge_data_thickness: EdgeData):

        def assert_self_edges_of_corner_vertices_have_zero_thickness(thickness):
            assert thickness == pytest.approx(0)

        assert edge_data_thickness.get_thickness() is not None

        assert len(edge_data_thickness.get_thickness()) == len(edge_data_thickness.get_ids_to_pos())
        assert len(edge_data_thickness.get_thickness()) == len(edge_data_thickness.cudf_frame)

        for (index, thickness) in edge_data_thickness.get_thickness().to_pandas().iteritems():
            try:
                assert thickness > 0
            except Exception as e:
                index_zero_thickness_edge = edge_data_thickness.cudf_frame.iloc[index]['source_vertex'][index]
                assert index_zero_thickness_edge == CONFIGURATIONS['corner_vertices']['fake_vertex_1'] or \
                       index_zero_thickness_edge == CONFIGURATIONS['corner_vertices']['fake_vertex_2']


    def test_set_lenghts(self, edge_data_lengths: EdgeData, graph_data_bound_pixel: GraphData):
        lengths = edge_data_lengths.get_lengths()
        assert len(lengths) == len(edge_data_lengths.cudf_frame)
        theoretical_longest_edge = calculate_diagonal_square_of_side(
            graph_data_bound_pixel.graph_space_bound.get_side())

        for i in range(0, len(lengths)):
            assert lengths[i] < theoretical_longest_edge
            try:
                assert lengths[i] > 0
            except Exception as e:
                if edge_data_lengths.cudf_frame[external_id('source')][i] == CONFIGURATIONS['corner_vertices'][
                    'fake_vertex_1'] or \
                        edge_data_lengths.cudf_frame[external_id('source')][i] == CONFIGURATIONS['corner_vertices'][
                    'fake_vertex_2']:
                    assert lengths[i] == 0
                else:
                    raise e
