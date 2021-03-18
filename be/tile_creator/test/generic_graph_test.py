import unittest

from be.tile_creator.src.graph.token_graph import TokenGraph


class GenericGraphTest(unittest.TestCase):
    '''
    Base class for tests
    '''

    graphs = []

    @classmethod
    def setUpClass(cls):
        # cls.graphs = [TokenGraph("../data/large.csv", {'dtype': {'amount': object}})]
        cls.graphs.append(TokenGraph("../data/medium.csv", {'dtype': {'amount': object}}))
        # cls.graphs.append(TokenGraph("../data/small.csv", {'dtype': {'amount': object}}))

    def test_graphs(self):
        for g in self.graphs:
            self.assertEqual(g.gpu_frame.nodes().shape[0], g.addresses_to_ids.shape[0])
