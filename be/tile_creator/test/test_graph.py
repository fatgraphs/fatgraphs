from be.tile_creator.test.generic_graph_test import GenericGraphTest


class GraphTest(GenericGraphTest):

    def test_loader_instanciation(self):
        self.assertIsNotNone(self.graphs)
        self.assertGreaterEqual(len(self.graphs), 1)

    def test_loader_has_data(self):
        for g in self.graphs:
            self.assertIsNotNone(g.raw_data)

    def test_map_addresses_to_ids(self):
        for g in self.graphs:
            g._map_addresses_to_ids()

    def test_make_graph_gpu_frame(self):
        for g in self.graphs:
            g._make_graph_gpu_frame(g.addresses_to_ids)
