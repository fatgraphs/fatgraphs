from typing import List
from unittest.mock import patch

from be.server.searches import SearchTerm
from be.server.searches.service import SearchTermService
from .interface import SearchTermInterface
from ..test.fixtures import app, db
from ..vertex_metadata.service import VertexMetadataService
import pandas as pd

def make_dataframe():
    return pd.DataFrame(
        columns=['type', 'label', 'other_column'],
        data=[  ["test_type", "test_label", "test_other"],
                ["test_type2", "test_label", "test_other"],
                ["test_type", "test_label2", "test_other"]])

class TestSearches:



    @patch.object(
            VertexMetadataService,
            "merge_graph_vertices_with_metadata",
            lambda graph_id, db : make_dataframe(),
        )

    def test_get_autocompletion_terms(db: object):
        result = SearchTermService.get_autocomplete_terms(1, db)

        assert len(result) == 4

        unique_types = list(filter(lambda e: e.type == 'type', result))
        assert len(unique_types) == 2
        assert "test_type" in map(lambda e: e.value, unique_types)
        assert "test_type2" in map(lambda e: e.value, unique_types)

        unique_labels = list(filter(lambda e: e.type == 'label', result))
        assert len(unique_labels) == 2
        assert "test_label" in map(lambda e: e.value, unique_labels)
        assert "test_label2" in map(lambda e: e.value, unique_labels)
