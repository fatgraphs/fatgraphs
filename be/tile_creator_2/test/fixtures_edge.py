from .fixtures_graph import *  # noqa
from .fixtures_vertex import *  # noqa
from .fixtures import *  # noqa

import pytest
from be.tile_creator_2.edge_data import EdgeData
from be.tile_creator_2.graph_data import GraphData
from be.tile_creator_2.gtm_args import GtmArgs
from be.tile_creator_2.vertex_data import VertexData


@pytest.fixture()
def edge_data(datasource):
    edge_data = EdgeData()
    yield edge_data


@pytest.fixture()
def edge_data_with_edges(datasource, edge_data, vertex_data_id):
    edge_data.set_cudf_frame(datasource, vertex_data_id)
    yield edge_data


@pytest.fixture()
def edge_data_positions(edge_data_with_edges: EdgeData, vertex_data_positions_fake: VertexData):
    edge_data_with_edges.set_ids_to_position(vertex_data_positions_fake)
    yield edge_data_with_edges


@pytest.fixture()
def edge_data_positions_pixel(edge_data_positions: EdgeData, vertex_data_positions_fake: VertexData):
    edge_data_positions.set_ids_to_pixel_position(vertex_data_positions_fake)
    yield edge_data_positions


@pytest.fixture()
def edge_data_thickness(edge_data_positions_pixel, graph_data_median: GraphData, gtm_args: GtmArgs):
    edge_data_positions_pixel.set_thickness(graph_data_median, gtm_args)
    yield edge_data_positions_pixel


@pytest.fixture()
def edge_data_lengths(edge_data_thickness: EdgeData):
    edge_data_thickness.set_lengths()
    yield edge_data_thickness
