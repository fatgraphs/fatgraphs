import pytest

from be.tile_creator.src.new_way.edge_data import EdgeData
from be.tile_creator.src.new_way.graph_data import GraphData
from be.tile_creator.src.new_way.gtm_args import GtmArgs
from be.tile_creator.src.new_way.test.fixtures_vertex import *
from be.tile_creator.src.new_way.test.fixtures import *
from be.tile_creator.src.new_way.test.fixtures_graph import *
from be.tile_creator.src.new_way.vertex_data import VertexData

@pytest.fixture()
def edge_data(datasource):
    edge_data = EdgeData()
    yield edge_data


@pytest.fixture()
def edge_data_with_edges(datasource, edge_data, vertex_data_id):
    edge_data.set_source_target_amount(datasource, vertex_data_id.get_vertex_to_id())
    yield edge_data


@pytest.fixture()
def edge_data_with_cudf_edges(edge_data_with_edges):
    edge_data_with_edges.populate_source_target_amount_cudf()
    yield edge_data_with_edges

@pytest.fixture()
def edge_data_positions(edge_data_with_cudf_edges: EdgeData, vertex_data_positions_fake: VertexData):
    edge_data_with_cudf_edges.set_ids_to_position(vertex_data_positions_fake.get_positions(cudf=True))
    yield edge_data_with_cudf_edges

@pytest.fixture()
def edge_data_positions_pixel(edge_data_positions: EdgeData, vertex_data_positions_fake: VertexData):
    edge_data_positions.set_ids_to_pixel_position(vertex_data_positions_fake.get_positions_pixel())
    yield edge_data_positions


@pytest.fixture()
def edge_data_thickness(edge_data_positions_pixel, graph_data_median: GraphData, gtm_args: GtmArgs):
    edge_data_positions_pixel.set_thickness(graph_data_median, gtm_args)
    yield edge_data_positions_pixel
