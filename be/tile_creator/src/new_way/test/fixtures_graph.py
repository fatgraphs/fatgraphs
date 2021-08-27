import pytest

from be.tile_creator.src.new_way.graph_data import GraphData
from be.tile_creator.src.new_way.gtm_args import GtmArgs
from be.tile_creator.src.new_way.test.fixtures_vertex import *
from be.tile_creator.src.new_way.test.fixtures_edge import *
from be.tile_creator.src.new_way.test.fixtures import *

@pytest.fixture()
def graph_data():
    yield GraphData()


@pytest.fixture()
def graph_data_bound(graph_data: GraphData, vertex_data_positions):
    graph_data.set_bounding_square(vertex_data_positions.get_positions())
    yield graph_data

@pytest.fixture()
def graph_data_bound_pixel(graph_data_bound: GraphData, gtm_args: GtmArgs):
    graph_data_bound.set_bounding_square_pixel(gtm_args)
    yield graph_data_bound

@pytest.fixture()
def graph_data_median(graph_data_bound_pixel: GraphData, vertex_data_positions_fake: VertexData):
    graph_data_bound_pixel.set_median_pixel_distance(vertex_data_positions_fake.get_positions_pixel())
    yield graph_data_bound_pixel
