from be.configuration import MEDIUM_GRAPH_RAW_PATH, SMALL_GRAPH_RAW_PATH, CONFIGURATIONS, MOCK_LABELLED_RAW_PATH, \
    LABELS_PATH, METADATA_PATH, LARGE_GRAPH_RAW_PATH
from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.src.render.edge_distribution_renderer import EdgeDistributionRenderer
from be.tile_creator.src.render.tiles_renderer import TilesRenderer
import os


from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator
from be.tile_creator.src.token_graph_metadata import TokenGraphMetadata


def main(configurations):
    graph = TokenGraph(configurations['source'], {'dtype': {'amount': float}})
    visual_layout = VisualLayout(graph, configurations['tile_size'],
                                 configurations['med_vertex_size'], configurations['max_vertex_size'],
                                 configurations['med_edge_thickness'], configurations['max_edge_thickness'])

    metadata = TokenGraphMetadata(graph, visual_layout, configurations)
    _generate_metadata_files(metadata, configurations)
    gt_graph = GraphToolTokenGraph(graph, visual_layout, metadata, configurations)

    transparency_calculator = TransparencyCalculator(visual_layout.edge_lengths_graph_space, configurations)

    tiles_renderer = TilesRenderer(gt_graph, visual_layout, metadata, transparency_calculator, configurations)

    ed_renderer = EdgeDistributionRenderer(configurations['zoom_levels'],
                                           visual_layout.edge_lengths_graph_space,
                                           transparency_calculator,
                                           configurations['output_folder'],
                                           visual_layout.max - visual_layout.min)
    ed_renderer.render()

    tiles_renderer.render()


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
