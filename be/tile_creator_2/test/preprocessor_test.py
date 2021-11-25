from .fixtures_edge import *  # noqa
from .fixtures_graph import *  # noqa
from .fixtures_vertex import *  # noqa
from .fixtures import *  # noqa

import pytest
import pandas as pd

from be.configuration import CONFIGURATIONS
from be.tile_creator_2.preprocessor import DataPreprocessor

class TestPreprocessor:

    @pytest.fixture()
    def preprocessor(self):
        yield DataPreprocessor()

    def test_fake_addresses_not_in_use_in_test_data(self, raw_data, preprocessor):

        try:
            preprocessor._check_fake_vertices_are_unused(raw_data)
        except Exception:
            assert False, "Fake addresses is in use"

    def test_check_fake_addresses_are_unused_throws(self, raw_data, preprocessor):
        raw_data = preprocessor._add_fake_vertices(raw_data)
        try:
            threw = True
            preprocessor._check_fake_vertices_are_unused(raw_data)
            threw = False
        except Exception:
            pass
        finally:
            assert threw, "fake vertices are present but this was NOT detected"

    def test_remove_parallel_edges(self, raw_data, preprocessor):
        original = len(raw_data)
        double_edges_count = original - raw_data[['source', 'target']].groupby(['source', 'target']).groups.__len__()

        after_removal = len(preprocessor._remove_parallel_edges(raw_data))
        assert original == after_removal + double_edges_count

    def test_add_fake_vertices(self, preprocessor):
        df = pd.DataFrame()
        vertices = preprocessor._add_fake_vertices(df)
        assert len(vertices) == 2

        expected_columns = ['source', 'target', 'amount', 'edgeType']
        assert len(vertices.columns) == len(expected_columns)
        assert all([a == b for a, b in zip(sorted(vertices.columns), sorted(expected_columns))])

    def test_fake_vertices_have_highest_id(self, raw_data, preprocessor):
        augmented_vertices = preprocessor._add_fake_vertices(raw_data)
        highest_id_prior_to_addition = raw_data.index.values.max()
        fake_address_1 = augmented_vertices.loc[augmented_vertices['source'] == CONFIGURATIONS['corner_vertices']['fake_vertex_1']]
        fake_address_2 = augmented_vertices.loc[augmented_vertices['source'] == CONFIGURATIONS['corner_vertices']['fake_vertex_2']]

        assert fake_address_1.index.values[0] == highest_id_prior_to_addition + 1
        assert fake_address_2.index.values[0] == highest_id_prior_to_addition + 2

