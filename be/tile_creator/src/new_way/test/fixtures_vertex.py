import pytest

from be.tile_creator.src.new_way.vertex_data import VertexData
from be.tile_creator.src.new_way.test.fixtures import *
from be.tile_creator.src.new_way.test.fixtures_graph import *
from be.tile_creator.src.new_way.test.fixtures_edge import *
from be.tile_creator.src.new_way.test.fixtures_graph import *


@pytest.fixture()
def vertex_data(datasource):
    vertex_data = VertexData()
    yield vertex_data


@pytest.fixture()
def vertex_data_id(datasource, vertex_data):
    vertex_data.set_vertex_to_ids(datasource)
    yield vertex_data


@pytest.fixture()
def vertex_data_degrees(vertex_data_id, cudf_graph):
    vertex_data_id.set_degrees(cudf_graph.get_graph())
    yield vertex_data_id


@pytest.fixture()
def vertex_data_positions(vertex_data_degrees, cudf_graph):
    vertex_data_degrees.set_positions(cudf_graph.get_graph())
    yield vertex_data_degrees


@pytest.fixture()
def vertex_data_positions_pixel(vertex_data_positions: VertexData, gtm_args: GtmArgs, graph_data_bound):
    vertex_data_positions.set_positions_pixel(gtm_args, graph_data_bound)
    yield vertex_data_positions


@pytest.fixture()
def vertex_data_positions_fake(vertex_data_positions_pixel, graph_data_bound_pixel):
    vertex_data_positions_pixel.set_fake_positions(graph_data_bound_pixel)
    yield vertex_data_positions_pixel
