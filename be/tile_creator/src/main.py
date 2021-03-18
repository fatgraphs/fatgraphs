from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.render.renderer import GraphRenderer

medium_graph = TokenGraph("../data/medium.csv", {'dtype': {'amount': object}})
renderer = GraphRenderer(medium_graph)
renderer.render_tiles(3)

