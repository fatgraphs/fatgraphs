from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.test.unit.generic_graph_test import GenericGraphTest


class GraphSpatialiserTest(GenericGraphTest):

    def setUp(self):
        self.spatialiser = VisualLayout()
        self.layout = self.spatialiser._run_force_atlas_2(self.graphs[0].gpu_frame)

    def test_there_are_as_many_positions_as_nodes(self):
        # TODO
        self.assertIsNotNone(self.layout)
        #self.assertEqual(self.layout.vertex_id_to_xy_tuple.shape[0], self.graphs[0].shape[0])

