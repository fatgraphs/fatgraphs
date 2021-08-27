from be.configuration import internal_id, external_id
from be.tile_creator.src.new_way.datasource import DataSource
from be.tile_creator.src.new_way.edge_data import EdgeData
from be.tile_creator.src.new_way.vertex_data import VertexData
from be.tile_creator.src.new_way.test.fixtures_vertex import *
from be.tile_creator.src.new_way.test.fixtures import *
from be.tile_creator.src.new_way.test.fixtures_graph import *
from be.tile_creator.src.new_way.test.fixtures_edge import *

class TestEdgeData:

    def test_set_source_target_amount(self, edge_data_with_edges: EdgeData, datasource: DataSource, vertex_data_id: VertexData):
        assert edge_data_with_edges.get_source_target_amount() is not None
        assert len(datasource.get_data()) == len(edge_data_with_edges.get_source_target_amount())
        for e in [external_id('source'), external_id('target'), 'amount']:
            assert e in edge_data_with_edges.get_source_target_amount().columns

    def test_ids_to_positions(self, edge_data_with_edges: EdgeData, vertex_data_positions: VertexData):
        assert edge_data_with_edges.get_ids_to_pos() is None, "at this stage edge data should NOT contain the " \
                                                                   "ids to position mappings "
        edge_data_with_edges.set_ids_to_position(vertex_data_positions.get_positions(cudf=True))

        assert edge_data_with_edges.get_ids_to_pos() is not None, "at this stage edge data SHOULD contain the " \
                                                                   "ids to position mappings "

        assert len(edge_data_with_edges.get_ids_to_pos()) == len(edge_data_with_edges.get_source_target_amount())

        assert internal_id("source") in edge_data_with_edges.get_ids_to_pos().columns
        assert internal_id("target") in edge_data_with_edges.get_ids_to_pos().columns
        assert external_id("source") in edge_data_with_edges.get_ids_to_pos().columns
        assert external_id("target") in edge_data_with_edges.get_ids_to_pos().columns

        assert "source_x" in edge_data_with_edges.get_ids_to_pos().columns
        assert "target_x" in edge_data_with_edges.get_ids_to_pos().columns
        assert "source_y" in edge_data_with_edges.get_ids_to_pos().columns
        assert "target_y" in edge_data_with_edges.get_ids_to_pos().columns

    def test_id_to_pixel_position(self, edge_data_positions_pixel: EdgeData):
        assert edge_data_positions_pixel.get_ids_to_pos(pixel=True) is not None
        assert len(edge_data_positions_pixel.get_ids_to_pos(pixel=True)) == \
               len(edge_data_positions_pixel.get_ids_to_pos())

        assert internal_id("source") in edge_data_positions_pixel.get_ids_to_pos(pixel=True).columns
        assert internal_id("target") in edge_data_positions_pixel.get_ids_to_pos(pixel=True).columns
        assert external_id("source") in edge_data_positions_pixel.get_ids_to_pos(pixel=True).columns
        assert external_id("target") in edge_data_positions_pixel.get_ids_to_pos(pixel=True).columns

        assert "source_x_pixel" in edge_data_positions_pixel.get_ids_to_pos(pixel=True).columns
        assert "target_x_pixel" in edge_data_positions_pixel.get_ids_to_pos(pixel=True).columns
        assert "source_y_pixel" in edge_data_positions_pixel.get_ids_to_pos(pixel=True).columns
        assert "target_y_pixel" in edge_data_positions_pixel.get_ids_to_pos(pixel=True).columns


    def test_set_thickness(self, edge_data_thickness: EdgeData, vertex_data_positions_fake: VertexData):
        assert edge_data_thickness.get_thickness() is not None

        assert len(edge_data_thickness.get_thickness()) == len(edge_data_thickness.get_ids_to_pos())
        assert len(edge_data_thickness.get_thickness()) == len(edge_data_thickness.get_source_target_amount())

        for (index, row) in edge_data_thickness.get_thickness().iterrows():
            if index >= len(edge_data_thickness.get_thickness()) - 2:
                assert row['thickness'] == pytest.approx(0)
            else:
                assert row['thickness'] > 0


