import unittest
import numpy as np
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.test.constants import TEST_DATA, TEST_FOLDER, UNIQUE_ADDRESSES, FAKE_NODES, PREPROCESSED_EDGES, \
    MEDIAN_VERTEX_DISTANCE
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

    def test_median_pixel_distance_is_in_ballpark(cls):
        cls.assertAlmostEqual(cls.layout.median_pixel_distance, MEDIAN_VERTEX_DISTANCE, delta=1.0)

    def test_vertices_with_higher_degree_have_larger_size(cls):
        # relying on indices of degrees to correspond to ids
        index_of_largest_vertex = cls.graph.degrees.idxmax()['out_degree']
        index_of_smallest_vertex = cls.graph.degrees.idxmin()['out_degree']
        largest = cls.layout.vertex_sizes[index_of_largest_vertex]
        smallest = cls.layout.vertex_sizes[index_of_smallest_vertex]
        cls.assertEqual(largest, cls.layout.vertex_sizes.max())
        cls.assertEqual(smallest, cls.layout.vertex_sizes.min())

    def test_edges_with_largest_amount_is_thickest(cls):
        # because of clipping we can get many values that are the largest thickness
        indexes_max_thickness = list(np.where(cls.layout.edge_thickness == cls.layout.edge_thickness.max())[0])
        index_highest_amount = cls.graph.edge_ids_to_amount['amount'].idxmax()
        cls.assertIn(index_highest_amount, indexes_max_thickness)

    def test_edges_with_smallest_amount_is_thinnest(cls):
        # because of clipping we can get many values that are the smallest thickness
        indexes_min_thickness = list(np.where(cls.layout.edge_thickness == cls.layout.edge_thickness.min())[0])
        index_min_amount = cls.graph.edge_ids_to_amount['amount'].idxmin()
        cls.assertIn(index_min_amount, indexes_min_thickness)