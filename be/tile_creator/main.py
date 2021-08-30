import os

from geoalchemy2 import Geometry

from be.configuration import CONFIGURATIONS, VERTEX_TABLE_NAME, SRID
from be.server import SessionLocal, engine
from be.server.graph.service import GraphService
from be.server.vertex.service import VertexService
from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.src.metadata.token_graph_metadata import TokenGraphMetadata
from be.tile_creator.src.render.tiles_renderer import TilesRenderer
from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator
from be.utils.utils import make_geoframe


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


    metadata = TokenGraphMetadata(graph, visualLayout, configurations)


    with SessionLocal() as db:
        from be.server.graph import Graph

        print("updating DB . . .")

        # save graph metadata to db
        new_graph = GraphService.create(metadata.get_config_dict(), db)

        # as soon as we have the id we can determine the graph folder
        graph_id = new_graph.id
        graph_name = configurations['graph_name']
        output_folder = mkdir_for_graph(graph_name, graph_id)
        GraphService.update(new_graph, {'output_folder': output_folder}, db)
        configurations['output_folder'] = output_folder

        # save vertices
        vertex_table = VERTEX_TABLE_NAME(graph_name, graph_id)
        VertexService.ensure_vertex_table_exists(vertex_table, graph_id)

        # this will be there
        vertices = graph.address_to_id.merge(visualLayout.vertexPositions)
        vertices = vertices.rename(columns={'address': 'eth'})
        vertices['size'] = visualLayout.vertexSizes
        vertices['graph_id'] = [str(graph_id)] * len(vertices)
        vertices = vertices.drop(columns=['vertex'])

        # save as geo frame
        geo_frame = make_geoframe(vertices)
        column_types = {'pos': Geometry('POINT', srid=SRID)}
        geo_frame.to_sql(vertex_table, engine, if_exists='append', index=False, dtype=column_types)

        print("generating vertices shapes . . .")
        visualLayout.vertexShapes = visualLayout.generate_shapes(db, graph_id)


    print("rendering tiles . . .")
    # this will be GraphToolTokenGraph(vertex_data, edge_data, graph_data)
    gtGraph = GraphToolTokenGraph(graph.edge_ids_to_amount, visualLayout, metadata, configurations['curvature'])
    tilesRenderer = TilesRenderer(gtGraph, metadata, configurations)
    tilesRenderer.renderGraph()

    # print("rendering edge distributions plots...")
    # edgePlotsRenderer = EdgeDistributionPlotRenderer(configurations, visualLayout)
    # edgePlotsRenderer.render()



if __name__ == '__main__':
    raise Exception("We are not supporting running main.py directly for tile generation, you should instead use " + \
                    "gtm.py as the entry point")
