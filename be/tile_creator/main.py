from be.persistency.persistence_api import persistenceApi
from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.src.metadata.token_graph_metadata import TokenGraphMetadata
from be.tile_creator.src.metadata.vertex_metadata import VerticesLabels
from be.tile_creator.src.render.edge_distribution_plot_renderer import EdgeDistributionPlotRenderer
from be.tile_creator.src.render.tiles_renderer import TilesRenderer
from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator


def main(configurations):
    graph = TokenGraph(configurations['source'], {'dtype': {'amount': float}})

    print("generating layout . . .")

    visualLayout = VisualLayout(graph, configurations)


    transparencyCalculator = TransparencyCalculator(visualLayout.max - visualLayout.min,
                                                     configurations)
    print("calculating edge transparencies . . .")

    visualLayout.edgeTransparencies = transparencyCalculator.calculateEdgeTransparencies(
        visualLayout.edgeLengths)

    print("generating vertices shapes . . .")



    metadata = TokenGraphMetadata(graph, visualLayout, configurations)

    persistenceApi.createMetadataTable(metadata)
    persistenceApi.createVertexTable(metadata.getGraphName(), visualLayout,
                                        graph.addressToId)

    vertices_metadata = VerticesLabels(configurations, graph.addressToId)
    visualLayout.vertexShapes = vertices_metadata.generate_shapes()

    gtGraph = GraphToolTokenGraph(graph.edgeIdsToAmount, visualLayout, metadata, configurations['curvature'])

    tilesRenderer = TilesRenderer(gtGraph, visualLayout, metadata, transparencyCalculator, configurations)

    edgePlotsRenderer = EdgeDistributionPlotRenderer(configurations, visualLayout)
    edgePlotsRenderer.render()
    print("rendering tiles . . .")
    tilesRenderer.renderGraph()


if __name__ == '__main__':
    raise Exception("We are not supporting running main.py directly for tile generation, you should instead use " + \
                    "gtm.py as the entry point")
