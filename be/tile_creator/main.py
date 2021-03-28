from be.configuration import MEDIUM_GRAPH_RAW_PATH, SMALL_GRAPH_RAW_PATH, CONFIGURATIONS, MOCK_LABELLED_RAW_PATH, \
    LABELS_PATH, METADATA_PATH
from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.render.renderer import GraphRenderer

medium_graph = TokenGraph(MOCK_LABELLED_RAW_PATH, {'dtype': {'amount': object}}, LABELS_PATH)
gt_graph = GraphToolTokenGraph(medium_graph)
renderer = GraphRenderer(gt_graph)
renderer.render_tiles(CONFIGURATIONS['zoom_levels'])

# post graph info to server


