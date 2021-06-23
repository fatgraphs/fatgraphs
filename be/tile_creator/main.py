from be.configuration import CONFIGURATIONS
from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.src.metadata.vertex_metadata import VerticesLabels
from be.persistency.db_connection import DbConnection
from be.persistency.persistence_api import PersistenceAPI, persistence_api
from be.tile_creator.src.render.edge_distribution_plot_renderer import EdgeDistributionPlotRenderer
from be.tile_creator.src.render.tiles_renderer import TilesRenderer
import os


from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator
from be.tile_creator.src.metadata.token_graph_metadata import TokenGraphMetadata


def main(configurations):
    graph = TokenGraph(configurations['source'], {'dtype': {'amount': float}})
    print("generating layout . . .")
    visual_layout = VisualLayout(graph, configurations)
    vertices_metadata = VerticesLabels(configurations, graph.address_to_id, visual_layout.vertex_positions)
    transparency_calculator = TransparencyCalculator(visual_layout.max - visual_layout.min,
                                                     configurations)
    print("calculating transparencies . . .")
    visual_layout.edge_transparencies = transparency_calculator.calculate_edge_transparencies(visual_layout.edge_lengths)
    visual_layout.vertex_shapes = vertices_metadata.generate_shapes()

    metadata = TokenGraphMetadata(graph, visual_layout, configurations)

    graph_name = metadata.get_graph_name()
    persistence_api.create_metadata_table(metadata)
    persistence_api.create_vertex_table(graph_name, visual_layout, vertices_metadata, graph.address_to_id)

    gt_graph = GraphToolTokenGraph(graph.edge_ids_to_amount, visual_layout, metadata, configurations['curvature'])


    tiles_renderer = TilesRenderer(gt_graph, visual_layout, metadata, transparency_calculator, configurations)

    ed_renderer = EdgeDistributionPlotRenderer(configurations['zoom_levels'],
                                               visual_layout.edge_lengths,
                                               visual_layout.edge_transparencies,
                                               configurations['output_folder'],
                                               visual_layout.max - visual_layout.min,
                                               configurations['tile_size'])
    ed_renderer.render()
    print("rendering tiles . . .")
    tiles_renderer.render()


if __name__ == '__main__':
    raise Exception("We are not supporting running main.py directly for tile generation, you should instead use " + \
                    "gtm.py as the entry point")
