import os

import geopandas as gpd
import requests
from geoalchemy2 import (
    Geometry,
    WKTElement,
)

from be.configuration import (
    EDGE_TABLE_NAME,
    SRID,
    TILE_FOLDER_NAME,
    VERTEX_TABLE_NAME,
    data_folder,
    external_id,
    graphs_home,
    internal_id,
)
from be.server import SessionLocal
from be.server.edge.service import EdgeService
from be.server.graph.interface import GraphInterface
from be.server.graph.service import GraphService
from be.server.graph_configuration.interface import GraphConfigurationInterface
from be.server.graph_configuration.service import GraphConfigurationService
from be.server.vertex.service import VertexService
from be.tile_creator_2.api.api import ApiLayer
from be.tile_creator_2.cudf_graph import CudfGraph
from be.tile_creator_2.datasource import DataSource
from be.tile_creator_2.edge_data import EdgeData
from be.tile_creator_2.edge_transparency_plots import EdgeTransparencyPlots
from be.tile_creator_2.graph_data import GraphData
from be.tile_creator_2.graph_tool_token_graph import GraphToolTokenGraph
from be.tile_creator_2.gtm_args import GtmArgs
from be.tile_creator_2.shape_calculator import ShapeGenerator
from be.tile_creator_2.tiles_renderer import TilesRenderer
from be.tile_creator_2.transparency_calculator import TransparencyCalculator
from be.tile_creator_2.vertex_data import VertexData
from be.utils import timeit


def mkdir_for_graph(graph_id: int):
    def ensure_directory_exists(path):
        if not os.path.exists(path):
            os.mkdir(path)

    ensure_directory_exists(graphs_home)
    graph_folder = TILE_FOLDER_NAME(graph_id)
    path = os.path.join(graphs_home, graph_folder)
    ensure_directory_exists(path)
    return path


def make_geoframe(frame):
    geo_frame = gpd.GeoDataFrame(frame, geometry=gpd.points_from_xy(frame.x, frame.y))
    geo_frame = geo_frame.drop(columns=['x', 'y'])
    geo_frame = geo_frame.rename_geometry('pos')
    geo_frame['pos'] = geo_frame['pos'].apply(lambda x: WKTElement(x.wkt, srid=SRID))
    return geo_frame

def main(configurations):
    args = GtmArgs(configurations)
    gtm_args = args

    # just reeads the csv
    source = DataSource(os.path.join(data_folder, gtm_args.get_source_file()))

    vertex_data = VertexData()
    edge_data = EdgeData()
    graph_data = GraphData()

    vertex_data.set_vertex_to_ids(source)
    edge_data.set_cudf_frame(source, vertex_data)

    cudf_graph = CudfGraph(edge_data.cudf_frame)

    vertex_data.set_degrees(cudf_graph.graph)
    vertex_data.set_positions(cudf_graph.graph)

    graph_data.set_graph_name(gtm_args)
    graph_data.set_graph_category(gtm_args)
    graph_data.set_edge_count(edge_data)
    graph_data.set_vertex_count(vertex_data)
    graph_data.set_description(gtm_args.get_description())

    with SessionLocal() as db:
        
        
        persisted_graph = ApiLayer.graph.post(graph_data.to_json_camelcase())
        # persisted_graph = GraphService.create(GraphInterface.from_graph_data(graph_data), db)

        graph_data.set_bounding_square(vertex_data)
        graph_data.set_bounding_square_pixel(gtm_args)

        vertex_data.set_positions_pixel(gtm_args, graph_data)

        vertex_data.set_corner_vertex_positions(graph_data)

        edge_data.set_ids_to_position(vertex_data)
        edge_data.set_ids_to_pixel_position(vertex_data)

        graph_data.set_median_pixel_distance(vertex_data)

        vertex_data.set_sizes(graph_data, gtm_args)

        edge_data.set_thickness(graph_data, gtm_args)
        edge_data.set_lengths()

        # TODO maybe move in
        tc = TransparencyCalculator(graph_data, gtm_args)
        transparencies = tc.calculateEdgeTransparencies(edge_data.get_lengths().to_numpy())
        edge_data.transparencies = transparencies

        # save the configuration to db
        # TODO save bound in graph_data: need to change FE code!

        config_obj = gtm_args.to_json_camel_case(graph_data, persisted_graph['id'])
        
        config_db = ApiLayer.configs.post(config_obj)

        # save vertices to db
        vertex_table = VERTEX_TABLE_NAME(persisted_graph['id'])
        VertexService.ensure_vertex_table_exists(vertex_table, persisted_graph['id'])

        f = vertex_data.cudf_frame.to_pandas()
        f['graph_id'] = persisted_graph['id']
        geo_frame = make_geoframe(f)
        print("geo_frame", geo_frame[['graph_id', 'vertex', 'size', 'pos']])
        geo_frame[['graph_id', 'vertex', 'size', 'pos']].to_sql(
            vertex_table,
            db.bind.engine,
            if_exists='append',
            index=False,
            dtype={'pos': Geometry('POINT', srid=SRID)})

        shg = ShapeGenerator(db, persisted_graph['id'])
        vertex_data = shg.augment_vertex_data(vertex_data)

        # save edges to db
        edge_table = EDGE_TABLE_NAME(persisted_graph['id'])
        EdgeService.ensure_edge_table_exists(edge_table, persisted_graph['id'])

        f = edge_data.cudf_frame.to_pandas()
        f['graph_id'] = persisted_graph['id']
        f = f.rename(columns={external_id('source'): 'src',
                              external_id('target'): 'trg'})
        f[['src', 'trg', 'amount', 'graph_id']].to_sql(edge_table,
                                                       db.bind.engine,
                                                       if_exists='append', index=False)

        gt_graph = make_gt_graph(edge_data, gtm_args, vertex_data)

        # as soon as we have the id we can make the graph folder
        output_folder = mkdir_for_graph(persisted_graph['id'])

        plotter = EdgeTransparencyPlots(graph_data, gtm_args, edge_data)
        plotter.render(output_folder)

        tr = TilesRenderer(gt_graph, output_folder, graph_data.get_graph_bound(), graph_data.get_pixel_bound())
        tr.render_graph()

@timeit("Constructing the graph_tool graph")
def make_gt_graph(edge_data, gtm_args, vertex_data):
    gt_graph = GraphToolTokenGraph()
    gt_graph.set_edges(edge_data.cudf_frame[[internal_id('source'), internal_id('target')]])
    gt_graph.set_vertex_position(vertex_data.get_positions())
    gt_graph.set_edge_length(edge_data.get_lengths())
    gt_graph.set_vertex_size(vertex_data.get_sizes())
    gt_graph.set_shapes(vertex_data.get_shapes())
    gt_graph.set_edge_thickness(edge_data.get_thickness())
    gt_graph.set_bezier_points(gtm_args.get_curvature())
    gt_graph.set_edge_transparencies(edge_data.get_transparencies())
    return gt_graph


