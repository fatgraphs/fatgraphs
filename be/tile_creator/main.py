import math
import os

import requests
import json

from be.configuration import CONFIGURATIONS
from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.src.metadata.token_graph_metadata import TokenGraphMetadata
from be.tile_creator.src.metadata.vertex_metadata import VerticesLabels
from be.tile_creator.src.render.tiles_renderer import TilesRenderer
from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)

def mkdir_for_graph(graph_name, graph_id):
    ensure_directory_exists(CONFIGURATIONS['graphsHome'])
    path = os.path.join(CONFIGURATIONS['graphsHome'])
    graph_folder = f'{graph_name}_{graph_id}'
    path = os.path.join(path, graph_folder)
    ensure_directory_exists(path)
    return path


def main(configurations):
    graph = TokenGraph(configurations['source'], {'dtype': {'amount': float}})

    print("generating layout . . .")
    visualLayout = VisualLayout(graph, configurations)

    print("calculating edge transparencies . . .")
    transparencyCalculator = TransparencyCalculator(visualLayout.max - visualLayout.min,
                                                     configurations)
    visualLayout.edgeTransparencies = transparencyCalculator.calculateEdgeTransparencies(
        visualLayout.edgeLengths)

    print("generating vertices shapes . . .")



    metadata = TokenGraphMetadata(graph, visualLayout, configurations)
    # TODO usernaem not hardcoded
    frame = metadata.getSingleFrame()
    body = frame.to_dict(orient='record')[0]
    response = requests.post("http://localhost:5000/tokengallery/graph/create", json=body)
    response = json.loads(response.text)

    graph_id = response['id']

    # as soon as we have the idd we can determine the graph folder
    output_folder = mkdir_for_graph(configurations['graphName'], graph_id)
    configurations['outputFolder'] =  output_folder
    response = requests.put(f"http://localhost:5000/tokengallery/graph/{graph_id}", json={'outputFolder': output_folder})


    vertices = graph.addressToId.merge(visualLayout.vertexPositions)
    vertices = vertices.rename(columns={'address': 'eth'})
    vertices['size'] = visualLayout.vertexSizes
    vertices['graphId'] = [graph_id] * len(vertices)
    vertices = vertices.drop(columns=['vertex'])
    for batch_dex in range(0, math.ceil(len(vertices) / 100)):
        dex = batch_dex * 100
        batch = vertices[dex:dex + 100]
        batch = batch.to_dict(orient='record')
        requests.post("http://localhost:5000/tokengallery/vertex/create", json=batch)

    # persistenceApi.createVertexTable(metadata.getGraphName(), visualLayout,
    #                                     graph.addressToId)

    vertices_metadata = VerticesLabels(configurations, graph.addressToId)
    visualLayout.vertexShapes = vertices_metadata.generate_shapes(graph_id)

    gtGraph = GraphToolTokenGraph(graph.edgeIdsToAmount, visualLayout, metadata, configurations['curvature'])

    tilesRenderer = TilesRenderer(gtGraph, visualLayout, metadata, transparencyCalculator, configurations)

    # edgePlotsRenderer = EdgeDistributionPlotRenderer(configurations, visualLayout)
    # edgePlotsRenderer.render()

    print("rendering tiles . . .")

    tilesRenderer.renderGraph()


if __name__ == '__main__':
    raise Exception("We are not supporting running main.py directly for tile generation, you should instead use " + \
                    "gtm.py as the entry point")
