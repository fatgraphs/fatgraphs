from be.configuration import MEDIUM_GRAPH_RAW_PATH, SMALL_GRAPH_RAW_PATH, CONFIGURATIONS, MOCK_LABELLED_RAW_PATH, \
    LABELS_PATH, METADATA_PATH, LARGE_GRAPH_RAW_PATH
from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.render.renderer import GraphRenderer
import os

from be.tile_creator.src.token_graph_metadata import TokenGraphMetadata


def main(csv_path, configuration_dictionary, labels_path=None):
    graph = TokenGraph(csv_path, {'dtype': {'amount': float}})
    metadata = TokenGraphMetadata(graph, configuration_dictionary, labels_path)
    gt_graph = GraphToolTokenGraph(graph, configuration_dictionary, metadata)

    _generate_metadata_files(metadata, configuration_dictionary)

    renderer = GraphRenderer(gt_graph, metadata, configuration_dictionary)
    renderer.render_tiles()


def _generate_metadata_files(metadata, configuration_dictionary):
    output_folder = configuration_dictionary['output_folder']
    metadata.vertices_metadata.to_csv(
        os.path.join(output_folder,
                     CONFIGURATIONS['vertices_metadata_file_name']), index=False)
    metadata.graph_metadata.to_csv(
        os.path.join(output_folder,
                     CONFIGURATIONS['graph_metadata_file_name']), index=False)


if __name__ == '__main__':
    configuration_dictionary = CONFIGURATIONS
    configuration_dictionary['output_folder'] = "be/graph-maps/testing-main"
    main(LARGE_GRAPH_RAW_PATH, configuration_dictionary)
