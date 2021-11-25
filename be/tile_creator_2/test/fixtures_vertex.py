from .fixtures_graph import *  # noqa
import pytest

from be.tile_creator_2.gtm_args import GtmArgs
from be.tile_creator_2.vertex_data import VertexData
from be.tile_creator_2.graph_data import GraphData


"""
The processing of the graph final output is a fully populated VertexData object.
Below are defined PARTIALLY POPULATED  instances of VertexData; they are used to test each
step of the processing separately. 
"""

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
    vertex_data_id.set_degrees(cudf_graph.graph)
    yield vertex_data_id


@pytest.fixture()
def vertex_data_positions(vertex_data_degrees, cudf_graph):
    vertex_data_degrees.set_positions(cudf_graph.graph)
    yield vertex_data_degrees


@pytest.fixture()
def vertex_data_positions_pixel(vertex_data_positions: VertexData, gtm_args: GtmArgs, graph_data_bound):
    vertex_data_positions.set_positions_pixel(gtm_args, graph_data_bound)
    yield vertex_data_positions


@pytest.fixture()
def vertex_data_positions_fake(vertex_data_positions_pixel, graph_data_bound_pixel):
    vertex_data_positions_pixel.set_corner_vertex_positions(graph_data_bound_pixel)
    yield vertex_data_positions_pixel

@pytest.fixture()
def vertex_data_size(vertex_data_positions_fake, graph_data_computed_properties: GraphData, gtm_args):
    vertex_data_positions_fake.set_sizes(graph_data_computed_properties, gtm_args)
    yield vertex_data_positions_fake
