from be.configuration import CONFIGURATIONS
from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.src.metadata.verticeslabels import VerticesLabels
from be.tile_creator.src.render.edge_distribution_plot_renderer import EdgeDistributionPlotRenderer
from be.tile_creator.src.render.tiles_renderer import TilesRenderer
import os


from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator
from be.tile_creator.src.metadata.token_graph_metadata import TokenGraphMetadata


def main(configurations):
    graph = TokenGraph(configurations['source'], {'dtype': {'amount': float}})
    print("generating layout . . .")
    visual_layout = VisualLayout(graph, configurations)
    vertices_labels = VerticesLabels(configurations, graph.address_to_id, visual_layout.vertex_positions)
    transparency_calculator = TransparencyCalculator(visual_layout.max - visual_layout.min,
                                                     configurations)
    print("calculating transparencies . . .")
    visual_layout.edge_transparencies = transparency_calculator.calculate_edge_transparencies(visual_layout.edge_lengths)
    visual_layout.vertex_shapes = vertices_labels.generate_vertiex_shapes()

    metadata = TokenGraphMetadata(graph, visual_layout, configurations, vertices_labels)
    _generate_metadata_files(metadata, configurations)
    gt_graph = GraphToolTokenGraph(graph.edge_ids_to_amount, visual_layout, metadata, configurations['curvature'])


    tiles_renderer = TilesRenderer(gt_graph, visual_layout, metadata, transparency_calculator, configurations)

    ed_renderer = EdgeDistributionPlotRenderer(configurations['zoom_levels'],
                                               visual_layout.edge_lengths,
                                               transparency_calculator,
                                               configurations['output_folder'],
                                               visual_layout.max - visual_layout.min,
                                               configurations['tile_size'])
    ed_renderer.render()
    print("rendering tiles . . .")
    tiles_renderer.render()


def _generate_metadata_files(metadata, configuration_dictionary):
    output_folder = configuration_dictionary['output_folder']
    metadata.vertices_labels.to_csv(
        os.path.join(output_folder,
                     CONFIGURATIONS['vertices_metadata_file_name']), index=False)
    metadata.graph_metadata.to_csv(
        os.path.join(output_folder,
                     CONFIGURATIONS['graph_metadata_file_name']), index=False)


if __name__ == '__main__':
    raise Exception("We are not supporting running main.py directly for tile generation, you should instead use " + \
                    "gtm.py as the entry point")
