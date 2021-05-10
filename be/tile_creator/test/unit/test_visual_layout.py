import unittest

from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.test.constants import TEST_DATA, TEST_FOLDER, UNIQUE_ADDRESSES, FAKE_NODES, PREPROCESSED_EDGES
from gtm import get_final_configurations


class TestVisualLayout(unittest.TestCase):

    graph = None
    layout = None

    @classmethod
    def setUpClass(cls):
        cls.graph = TokenGraph(TEST_DATA, {'dtype': {'amount': object}})
        default_config = get_final_configurations({'--csv': TEST_DATA}, TEST_FOLDER, "test_graph")
        cls.layout = VisualLayout(cls.graph, default_config)

    def test_fa2_has_produced_coordinates(cls):
        cls.assertIsNotNone(cls.layout.vertex_positions)
        cls.assertEqual(cls.layout.vertex_positions.shape[0], UNIQUE_ADDRESSES + FAKE_NODES)

    def test_fake_node_are_top_left_and_bottom_right(cls):
        max_id = cls.graph.address_to_id['vertex'].max()
        max_id_2 = max_id - 1
        top_left = list(cls.layout.vertex_positions[max_id:max_id + 1][['x', 'y']].values[0])
        bottom_right = list(cls.layout.vertex_positions[max_id_2:max_id_2 + 1][['x', 'y']].values[0])
        actual_top_left  = [cls.layout.min] * 2
        actual_botttom_right = [cls.layout.max] * 2
        cls.assertListEqual(top_left, actual_top_left)
        cls.assertListEqual(bottom_right, actual_botttom_right)

    def test_layout_is_square(cls):
        bottom_right = cls.layout.vertex_positions[['x', 'y']].max()
        top_left = cls.layout.vertex_positions[['x', 'y']].min()
        cls.assertEqual(bottom_right['x'], bottom_right['y'])
        cls.assertEqual(top_left['x'], top_left['y'])

    def test_edge_ids_to_positions_are_as_many_as_the_edges(cls):
        cls.assertEqual(cls.layout.edge_ids_to_positions.shape[0], PREPROCESSED_EDGES + FAKE_NODES)

    def test_pixel_coordinates_are_within_tile_bounds(cls):
        pixel_max = cls.layout.edge_ids_to_positions_pixel.max()
        pixel_min = cls.layout.edge_ids_to_positions_pixel.min()
        cls.assertTrue(pixel_max['source_x_pixel'] == pixel_max['source_y_pixel'] == pixel_max['target_x_pixel']
                       == pixel_max['target_y_pixel'])
        cls.assertTrue(pixel_min['source_x_pixel'] == pixel_min['source_y_pixel'] == pixel_min['target_x_pixel']
                       == pixel_min['target_y_pixel'])
