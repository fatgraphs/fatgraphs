import os
from be.tile_creator.src.new_way.cudf_graph import CudfGraph
from be.tile_creator.src.new_way.datasource import _load_csv, DataSource
from be.tile_creator.src.new_way.test.fixtures_vertex import *
from be.tile_creator.src.new_way.test.fixtures_edge import *
from be.tile_creator.src.new_way.test.fixtures_graph import *
import pandas as pd

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DATA = os.path.join(TEST_DIR, "../../test/test_graph.csv")
TEST_OUTPUT_DIR = os.path.join(TEST_DIR, "../../test/output")
TEST_REFERENCE_OUTPUT_DIR = os.path.join(TEST_DIR, "../../test/reference_output")
IMG_SIMILARITY_DIR = os.path.join(TEST_DIR, "../../test/img_similarity")
SMALL_SIMILAR_GRAPHS_DIR = os.path.join(IMG_SIMILARITY_DIR, 'small')
MEDIUM_SIMILAR_GRAPHS_DIR = os.path.join(IMG_SIMILARITY_DIR, 'medium')
RAW_EDGES = 278
PREPROCESSED_EDGES = 252
UNIQUE_ADDRESSES = 197
FAKE_NODES = 2
FAKE_EDGES = FAKE_NODES  # each fake nodes has a self-edge to itself

@pytest.fixture()
def gtm_args():
    yield GtmArgs()


@pytest.fixture()
def csv_path():
    yield TEST_DATA


@pytest.fixture()
def raw_data(csv_path):
    yield _load_csv(csv_path)


@pytest.fixture()
def datasource(csv_path):
    yield DataSource(csv_path)


@pytest.fixture()
def cudf_graph(edge_data_with_cudf_edges):
    yield CudfGraph(edge_data_with_cudf_edges.get_source_target_amount(cudf=True))

@pytest.fixture()
def graph_data():
    yield GraphData()


@pytest.fixture()
def graph_data_bound(graph_data, vertex_data_positions):
    graph_data.set_max_coordinate(vertex_data_positions.get_positions())
    graph_data.set_min_coordinate(vertex_data_positions.get_positions())
    yield graph_data


def get_vertices_from_file():
    nested_vertices_from_file = pd.read_csv(TEST_DATA)[['source', 'target']].values
    flat_vertices_from_file = [item for sublist in nested_vertices_from_file for item in sublist]
    return flat_vertices_from_file