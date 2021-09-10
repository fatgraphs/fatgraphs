import unittest
from be.configuration import CONFIGURATIONS
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.new_way.test.fixtures import TEST_DATA, RAW_EDGES, FAKE_EDGES, PREPROCESSED_EDGES, UNIQUE_ADDRESSES, FAKE_NODES


class TestTokenGraph(unittest.TestCase):
    '''
    Base class for tests
    '''
    graph = None

    @classmethod
    def setUpClass(cls):
        cls.graph = TokenGraph(TEST_DATA, {'dtype': {'amount': object}})

    def test_it_loaded(cls):
        cls.assertIsNotNone(cls.graph)

    def test_number_of_raw_edges_is_expected(cls):
        cls.assertEqual(cls.graph.raw_data.shape[0], RAW_EDGES)

    def test_number_of_preprocessed_edges_is_expected(cls):
        # each fake node has a fake edge to itself
        cls.assertEqual(cls.graph.preprocessed_data.shape[0], PREPROCESSED_EDGES + FAKE_EDGES)

    def test_number_of_unique_addresses_is_expected(cls):
        cls.assertEqual(cls.graph.address_to_id.shape[0], UNIQUE_ADDRESSES + FAKE_NODES)

    def test_edge_to_amount_map_has_expected_number_of_edges(cls):
        cls.assertEqual(cls.graph.edge_ids_to_amount.shape[0], PREPROCESSED_EDGES + FAKE_EDGES)

    def test_fake_nodes_have_highest_ids(cls):
        highest_id = cls.graph.address_to_id['index'].max()
        fake_address_1 = cls.graph.address_to_id.where(cls.graph.address_to_id['index'] == highest_id - 1)['vertex'].dropna().values[0]
        fake_address_2 = cls.graph.address_to_id.where(cls.graph.address_to_id['index'] == highest_id)['vertex'].dropna().values[0]
        cls.assertEqual(fake_address_1, CONFIGURATIONS['corner_vertices']['fake_vertex_1'])
        cls.assertEqual(fake_address_2, CONFIGURATIONS['corner_vertices']['fake_vertex_2'])

    def test_edge_to_amount_map_is_equivalent_to_the_cudf_version(cls):
        cls.assertIsNotNone(cls.graph.edge_ids_to_amount_cudf)
        cls.assertTrue(all(cls.graph.edge_ids_to_amount_cudf.to_pandas() == cls.graph.edge_ids_to_amount))

    def test_there_are_as_many_vertices_as_degrees(cls):
        degreeCount = cls.graph.degrees.shape[0]
        addressCount = UNIQUE_ADDRESSES + FAKE_NODES
        cls.assertEqual(degreeCount, addressCount)