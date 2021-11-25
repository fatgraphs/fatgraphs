from .fixtures_vertex import *  # noqa
from .fixtures import * # noqa
from .fixtures_edge import *  # noqa

import pytest

from be.tile_creator_2.edge_data import EdgeData
from be.tile_creator_2.graph_data import GraphData
from be.tile_creator_2.gtm_args import GtmArgs
from be.tile_creator_2.vertex_data import VertexData

@pytest.fixture()
def graph_data():
    yield GraphData()


@pytest.fixture()
def graph_data_bound(graph_data: GraphData, vertex_data_positions):
    graph_data.set_bounding_square(vertex_data_positions)
    yield graph_data

@pytest.fixture()
def graph_data_bound_pixel(graph_data_bound: GraphData, gtm_args: GtmArgs):
    graph_data_bound.set_bounding_square_pixel(gtm_args)
    yield graph_data_bound

@pytest.fixture()
def graph_data_median(graph_data_bound_pixel: GraphData, vertex_data_positions_fake: VertexData):
    graph_data_bound_pixel.set_median_pixel_distance(vertex_data_positions_fake)
    yield graph_data_bound_pixel

@pytest.fixture()
def graph_data_computed_properties(graph_data_bound_pixel: GraphData,
                                   vertex_data_positions_fake: VertexData,
                                   edge_data_thickness: EdgeData,
                                   gtm_args: GtmArgs):
    graph_data_bound_pixel.set_graph_name(gtm_args)
    graph_data_bound_pixel.set_vertex_count(vertex_data_positions_fake)
    graph_data_bound_pixel.set_edge_count(edge_data_thickness)
    yield graph_data_bound_pixel
