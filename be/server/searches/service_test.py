from typing import List
from unittest.mock import patch

from be.server.searches import SearchTerm
from be.server.searches.service import SearchTermService
from .interface import SearchTermInterface
from ..test.fixtures import app, db
from ..vertex_metadata.service import VertexMetadataService


class TestSearches:

    @patch.object(
            VertexMetadataService,
            "get_unique_types",
            lambda page, db : ['test_1'
            ],
        )
    @patch.object(
            VertexMetadataService,
            "get_unique_labels",
            lambda page, db : ['test_2'
            ],
        )
    def test_get_autocompletion_terms(db: object):
        result: List[str] = SearchTermService.get_autocomplete_terms(1, db)

        assert len(result) == 2
        test_type = list(filter(lambda e: e.type == 'type', result))
        assert len(test_type) == 1
        assert test_type[0].value == 'test_1'
        test_label = list(filter(lambda e: e.type == 'label', result))
        assert len(test_label) == 1
        assert test_label[0].value == 'test_2'
