import unittest
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.test.constants import TEST_DATA, PREPROCESSED_EDGES, RAW_EDGES, UNIQUE_ADDRESSES, FAKE_NODES, \
    FAKE_EDGES


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
        cls.assertEqual(cls.graph.rawData.shape[0], RAW_EDGES)

    def test_number_of_preprocessed_edges_is_expected(cls):
        # each fake node has a fake edge to itself
        cls.assertEqual(cls.graph.preprocessedData.shape[0], PREPROCESSED_EDGES + FAKE_EDGES)

    def test_number_of_unique_addresses_is_expected(cls):
        cls.assertEqual(cls.graph.addressToId.shape[0], UNIQUE_ADDRESSES + FAKE_NODES)

    def test_edge_to_amount_map_has_expected_number_of_edges(cls):
        cls.assertEqual(cls.graph.edgeIdsToAmount.shape[0], PREPROCESSED_EDGES + FAKE_EDGES)

    def test_fake_nodes_have_highest_ids(cls):
        highest_id = cls.graph.addressToId['vertex'].max()
        fake_address_1 = cls.graph.addressToId.where(cls.graph.addressToId.vertex == highest_id -1)['address'].dropna().values[0]
        fake_address_2 = cls.graph.addressToId.where(cls.graph.addressToId.vertex == highest_id)['address'].dropna().values[0]
        cls.assertEqual(fake_address_1, cls.graph.preprocessor.FAKE_ADDRESS1)
        cls.assertEqual(fake_address_2, cls.graph.preprocessor.FAKE_ADDRESS2)

    def test_edge_to_amount_map_is_equivalent_to_the_cudf_version(cls):
        cls.assertIsNotNone(cls.graph.edgeIdsToAmountCudf)
        cls.assertTrue(all(cls.graph.edgeIdsToAmountCudf.to_pandas() == cls.graph.edgeIdsToAmount))

    def test_there_are_as_many_vertices_as_degrees(cls):
        degreeCount = cls.graph.degrees.shape[0]
        addressCount = UNIQUE_ADDRESSES + FAKE_NODES
        cls.assertEqual(degreeCount, addressCount)