import unittest
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.test.constants import TEST_DATA_DIR, PREPROCESSED_EDGES, RAW_EDGES, UNIQUE_ADDRESSES, FAKE_NODES, \
    FAKE_EDGES


class TestTokenGraph(unittest.TestCase):
    '''
    Base class for tests
    '''
    graph = None

    @classmethod
    def setUpClass(cls):
        cls.graph = TokenGraph(TEST_DATA_DIR, {'dtype': {'amount': object}})

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
        highest_id = cls.graph.address_to_id['vertex'].max()
        fake_address_1 = cls.graph.address_to_id.where(cls.graph.address_to_id.vertex == highest_id -1)['address'].dropna().values[0]
        fake_address_2 = cls.graph.address_to_id.where(cls.graph.address_to_id.vertex == highest_id)['address'].dropna().values[0]
        cls.assertEqual(fake_address_1, cls.graph.preprocessor.FAKE_ADDRESS1)
        cls.assertEqual(fake_address_2, cls.graph.preprocessor.FAKE_ADDRESS2)

    def test_edge_to_amount_map_is_equivalent_to_the_cudf_version(cls):
        cls.assertIsNotNone(cls.graph.edge_ids_to_amount_cudf)
        cls.assertTrue(all(cls.graph.edge_ids_to_amount_cudf.to_pandas() == cls.graph.edge_ids_to_amount))

    def test_there_are_as_many_vertices_as_degrees(cls):
        degree_count = cls.graph.degrees.shape[0]
        address_count = UNIQUE_ADDRESSES + FAKE_NODES
        cls.assertEqual(degree_count, address_count)