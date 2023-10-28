import json
import math
import os
import cudf
import pandas as pd
import geopandas as gpd
from geoalchemy2 import (
    WKTElement,
)

from be.configuration import (
    SRID,
    TILE_FOLDER_NAME,
    data_folder,
    external_id,
    graphs_home,
    internal_id,
)

from be.tile_creator_2.api.api import ApiLayer
from be.tile_creator_2.cudf_graph import CudfGraph
from be.tile_creator_2.datasource import DataSource
from be.tile_creator_2.edge_data import EdgeData
from be.tile_creator_2.edge_transparency_plots import EdgeTransparencyPlots
from be.tile_creator_2.graph_data import GraphData
from be.tile_creator_2.graph_tool_token_graph import GraphToolTokenGraph
from be.tile_creator_2.gtm_args import GtmArgs
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
        
    persisted_graph = ApiLayer.graph.post(graph_data.to_json_camelcase())

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

    tc = TransparencyCalculator(graph_data, gtm_args)
    transparencies = tc.calculateEdgeTransparencies(edge_data.get_lengths().to_numpy())
    edge_data.transparencies = transparencies

    # save the configuration to db
    # TODO save bound in graph_data: need to change FE code!
    config_obj = gtm_args.to_json_camel_case(graph_data, persisted_graph['id'])
    ApiLayer.configs.post(config_obj)

    df_edges = vertex_data.cudf_frame.to_pandas()
    df_edges['graph_id'] = persisted_graph['id']
    geo_frame = make_geoframe(df_edges)

    ApiLayer.vertices.post_stream(
        geo_frame[['graph_id', 'vertex', 'size', 'pos']]
    )

    # fetch all the vertices metadata
    res = ApiLayer.vertex_metadata.get_all_for_graph(persisted_graph['id'])

    int_to_icon = {
            0: 'inactive_fake',
            1: 'eoa_unlabelled',
            2: 'eoa_labelled',
            3: 'ca_unlabelled',
            4: 'ca_labelled'
        }
    
    # TODO make it so after N row it merges them to the frame
    # iin this way we won't trash  memory. Right now we are loading into 
    # memory everything 
    vertex_metadata_subset = []
    for row in res.iter_lines(chunk_size=1):
        row = json.loads(row.decode())

        code = math.nan
        
        if row['account_type'] is not None:
            code = (row['account_type'] * 2) + 1
            code += 1 if row['label'] else 0
            code = int_to_icon[code]

        if row['icon'] is not None:
            code = row['icon']

        vertex_metadata_subset.append(
            dict(vertex=row['vertex'], code=code)
        )

    vertex_metadata_subset = pd.DataFrame.from_records(vertex_metadata_subset)
    vertex_metadata_subset = cudf.DataFrame.from_pandas(vertex_metadata_subset)

    if vertex_metadata_subset.empty:
        vertex_metadata_subset = cudf.DataFrame(columns=['vertex', 'code'])

    vertex_df_augmented = vertex_data.cudf_frame.merge(
        vertex_metadata_subset, 
        on='vertex', 
        how='left'
    )

    vertex_df_augmented.fillna('inactive_fake', inplace=True)

    vertex_data.cudf_frame = vertex_df_augmented

    # save edges to db
    df_edges = edge_data.cudf_frame.to_pandas()
    df_edges['graph_id'] = persisted_graph['id']
    df_edges = df_edges.rename(columns={external_id('source'): 'src',
                            external_id('target'): 'trg'})
    
    ApiLayer.edges.post_stream(
        df_edges[['src', 'trg', 'amount', 'graph_id']]
    )

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


