from be.configuration import MEDIUM_GRAPH_RAW_PATH, SMALL_GRAPH_RAW_PATH, CONFIGURATIONS, MOCK_LABELLED_RAW_PATH, \
    LABELS_PATH, METADATA_PATH
from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.render.renderer import GraphRenderer


def main(csv_path, configuration_dictionary, labels_path=None):
    graph = TokenGraph(csv_path, {'dtype': {'amount': object}}, labels_path)

    # TODO add support for lables
    # regenerate metadata because positions may have changed
    if labels_path is not None:
        metadata = graph.nodes_metadata.drop_duplicates()
        metadata.to_csv(METADATA_PATH, index=False)

    gt_graph = GraphToolTokenGraph(graph)
    renderer = GraphRenderer(gt_graph)
    renderer.render_tiles(configuration_dictionary['zoom_levels'])

    # post graph info to server


if __name__ == '__main__':
    main(MEDIUM_GRAPH_RAW_PATH, CONFIGURATIONS)
