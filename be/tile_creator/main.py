from be.configuration import MEDIUM_GRAPH_RAW_PATH, SMALL_GRAPH_RAW_PATH, CONFIGURATIONS, MOCK_LABELLED_RAW_PATH, \
    LABELS_PATH, METADATA_PATH, LARGE_GRAPH_RAW_PATH
from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.render.renderer import GraphRenderer
import os

from be.tile_creator.src.token_graph_metadata import TokenGraphMetadata


def main(configurations):
    graph = TokenGraph(configurations['source'], {'dtype': {'amount': float}})
    metadata = TokenGraphMetadata(graph, configurations)
    gt_graph = GraphToolTokenGraph(graph, configurations, metadata)

    _generate_metadata_files(metadata, configurations)

    renderer = GraphRenderer(gt_graph, metadata, configurations)
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
    raise Exception("We are not supporting running main.py directly for tile generation, you should instead use " + \
                    "gtm.py as the entry point")
