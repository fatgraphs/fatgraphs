from be.tile_creator.src.render.tiles_renderer import TilesRenderer
from be.tile_creator.test.unit.generic_graph_test import GenericGraphTest


class GraphRendererTest(GenericGraphTest):

    def setUp(self):
        self.renderer = TilesRenderer(self.graphs[0])

    #
    # def test_render_single_tile(self):
    #     return self.renderer._render(1)

    def test_render_all(self):
        return self.renderer.render(2)
