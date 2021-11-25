import os

import pytest

from be.tile_creator_2.cudf_graph import CudfGraph
from be.tile_creator_2.datasource import _load_csv, DataSource
import pandas as pd

from be.tile_creator_2.gtm_args import GtmArgs
from commands.gtm import get_final_configurations

from .fixtures_edge import *  # noqa

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DATA = os.path.join(TEST_DIR, "data/test_graph.csv")

@pytest.fixture()
def configurations():
    test_graph_id = 54
    test_graph_name = "test_name"
    raw_args_test = {"--csv": "test/path/file.csv"}
    configurations = get_final_configurations(raw_args_test, test_graph_name, test_graph_id)
    yield configurations

@pytest.fixture()
def gtm_args(configurations):
    yield GtmArgs(configurations)


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
def cudf_graph(edge_data_with_edges):
    yield CudfGraph(edge_data_with_edges.cudf_frame)


def get_vertices_from_file():
    nested_vertices_from_file = pd.read_csv(TEST_DATA)[['source', 'target']].values
    flat_vertices_from_file = [item for sublist in nested_vertices_from_file for item in sublist]
    return flat_vertices_from_file