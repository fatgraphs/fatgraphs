from be.tile_creator.src.layout.layout_generator import LayoutGenerator
from be.tile_creator.test.generic_graph_test import GenericGraphTest


class GraphSpatialiserTest(GenericGraphTest):

    def setUp(self):
        self.spatialiser = LayoutGenerator()
        self.layout = self.spatialiser._run_force_atlas_2(self.graphs[0].gpu_frame)

    def test_there_are_as_many_positions_as_nodes(self):
        # TODO
        self.assertIsNotNone(self.layout)
        #self.assertEqual(self.layout.vertex_id_to_xy_tuple.shape[0], self.graphs[0].shape[0])
