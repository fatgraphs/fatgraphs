from be.tile_creator.src.render.renderer import GraphRenderer
from be.tile_creator.test.generic_graph_test import GenericGraphTest


class GraphRendererTest(GenericGraphTest):

    def setUp(self):
        self.renderer = GraphRenderer(self.graphs[0])

    #
    # def test_render_single_tile(self):
    #     return self.renderer._render(1)

    def test_render_all(self):
        return self.renderer.render_tiles(2)
