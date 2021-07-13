import unittest
import numpy as np
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.test.constants import TEST_DATA, TEST_DIR, UNIQUE_ADDRESSES, FAKE_NODES, PREPROCESSED_EDGES
from gtm import get_final_configurations
import math

class TestVisualLayout(unittest.TestCase):

    graph = None
    layout = None

    @classmethod
    def setUpClass(cls):
        cls.graph = TokenGraph(TEST_DATA, {'dtype': {'amount': object}})
        default_config = get_final_configurations({'--csv': TEST_DATA}, TEST_DIR, "test_graph")
        cls.layout = VisualLayout(cls.graph, default_config)

    def test_each_address_has_a_coordinate(cls):
        cls.assertIsNotNone(cls.layout.vertex_positions)
        cls.assertEqual(cls.layout.vertex_positions.shape[0], UNIQUE_ADDRESSES + FAKE_NODES)

    def test_fake_node_are_top_left_and_bottom_right(cls):
        bottom_right_vertex_pos, top_left_vertex_pos = cls._get_position_fake_nodes()
        expected_top_left_vertex_pos = [cls.layout.min] * 2
        expected_bottom_right_vertex_pos = [cls.layout.max] * 2
        cls.assertListEqual(top_left_vertex_pos, expected_top_left_vertex_pos)
        cls.assertListEqual(bottom_right_vertex_pos, expected_bottom_right_vertex_pos)

    def test_there_are_other_nodes_that_share_one_of_the_coordinate_of_the_fake_nodes(cls):
        """
        This test ensure that the position of the fake nodes is coherent wrt position of the other 'real nodes'.
        """

        bottom_right_vertex_pos, top_left_vertex_pos = cls._get_position_fake_nodes()
        # the fake nodes are always the last two
        real_nodes = cls.layout.vertex_positions[0:-2]
        single_values_real_nodes = real_nodes[['x', 'y']].values.flatten()
        cls.assertTrue(bottom_right_vertex_pos[0] in single_values_real_nodes and
                       bottom_right_vertex_pos[1] in single_values_real_nodes and
                       top_left_vertex_pos[0] in single_values_real_nodes and
                       top_left_vertex_pos[1] in single_values_real_nodes)

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
        cls.assertTrue(pixel_max['sourceXPixel'] == pixel_max['sourceYPixel'] == pixel_max['targetXPixel']
                       == pixel_max['targetYPixel'])
        cls.assertTrue(pixel_min['sourceXPixel'] == pixel_min['sourceYPixel'] == pixel_min['targetXPixel']
                       == pixel_min['targetYPixel'])

    def test_vertex_with_highest_degree_has_largest_size(cls):
        # relying on indices of degrees to correspond to ids
        index_of_largest_vertex = cls.graph.degrees.idxmax()['outDegree']
        largest = cls.layout.vertex_sizes[index_of_largest_vertex]
        cls.assertEqual(largest, cls.layout.vertex_sizes.max())

    def test_vertex_with_smallest_degree_has_smallest_size(cls):
        # relying on indices of degrees to correspond to ids
        index_of_smallest_vertex = cls.graph.degrees.idxmin()['outDegree']
        smallest = cls.layout.vertex_sizes[index_of_smallest_vertex]
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

    def test_edge_lengths_are_right_order(cls):
        """
        Edge lengths should be in such an order that they match the order of the edge list.
        I.E. element i in the edge_lenghts corresponds to the length of edge i in the edge list.
        :return:
        """
        edge_lengths = cls.layout.edge_lengths
        vertex_positions = cls.layout.vertex_positions
        for index, edge in cls.graph.edge_ids_to_amount.iterrows():
            source = vertex_positions[['x', 'y']].iloc[int(edge.sourceId)]
            target = vertex_positions[['x', 'y']].iloc[int(edge.targetId)]
            source = [source['x'], source['y']]
            target = [target['x'], target['y']]
            expected_edge_length = math.dist(source, target)
            actual_edge_length = edge_lengths[index]
            cls.assertAlmostEqual(expected_edge_length, actual_edge_length, delta=0.001)

    def _get_position_fake_nodes(cls):
        max_id = cls.graph.address_to_id['vertex'].max()
        max_id_2 = max_id - 1
        top_left_vertex_pos = list(cls.layout.vertex_positions[max_id:max_id + 1][['x', 'y']].values[0])
        bottom_right_vertex_pos = list(cls.layout.vertex_positions[max_id_2:max_id_2 + 1][['x', 'y']].values[0])
        return bottom_right_vertex_pos, top_left_vertex_pos

