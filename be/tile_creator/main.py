from be.configuration import MEDIUM_GRAPH_RAW_PATH, SMALL_GRAPH_RAW_PATH, CONFIGURATIONS, MOCK_LABELLED_RAW_PATH, \
    LABELS_PATH, METADATA_PATH
from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.render.renderer import GraphRenderer
import os

def main(csv_path, configuration_dictionary, labels_path=None):

    graph = TokenGraph(csv_path, {'dtype': {'amount': float}}, labels_path)
    gt_graph = GraphToolTokenGraph(graph)

    _generate_metadata_files(configuration_dictionary, graph)

    renderer = GraphRenderer(gt_graph, configuration_dictionary)
    renderer.render_tiles()


def _generate_metadata_files(configuration_dictionary, graph):
    output_folder = configuration_dictionary['output_folder']
    graph.vertices_metadata.to_csv(os.path.join(output_folder, CONFIGURATIONS['vertices_metadata_file_name']),
                                   index=False)
    graph.graph_metadata.to_csv(os.path.join(output_folder, CONFIGURATIONS['graph_metadata_file_name']), index=False)


if __name__ == '__main__':
    main(MEDIUM_GRAPH_RAW_PATH, CONFIGURATIONS)
