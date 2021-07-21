from unittest.mock import patch
from flask.testing import FlaskClient

from ..test.fixtures import client, app  # noqa

from .schema import SearchTermSchema
from .service import SearchTermService
from .model import SearchTerm
from . import BASE_ROUTE


def make_search(
    id: int = 123, type: str = "Test widget", value: str = "Test purpose"
) -> SearchTerm:
    return SearchTerm(id=id, type=type, value=value)


class TestRecentSearchTermsResource:
    @patch.object(
        SearchTermService,
        "get_recent_searches",
        lambda db : [
            make_search(123, type="Test Widget 1", value='idex'),
            make_search(456, type="Test Widget 2", value='dex'),
        ],
    )
    def test_get(self, client: FlaskClient):
        with client:
            results = client.get(f"/tokengallery/{BASE_ROUTE}", follow_redirects=True).get_json()
            expected = (
                SearchTermSchema(many=True)
                .dump(
                    [
                        make_search(123, type="Test Widget 1", value='idex'),
                        make_search(456, type="Test Widget 2", value='dex'),make_search(123, type="Test Widget 1", value='idex'),
                    ]
                )
                
            )
            for r in results:
                assert r in expected

    @patch.object(
        SearchTermService, "update_search_terms", lambda create_request, db: [SearchTerm(**create_request)]
    )
    def test_put(self, client: FlaskClient):  # noqa
        with client:

            payload = dict(type="Test widget", value="Test purpose")
            result = client.put(f"/tokengallery/{BASE_ROUTE}", json=payload).get_json()
            expected = (
                SearchTermSchema(many=True)
                .dump([SearchTerm(type=payload["type"], value=payload["value"])])

            )
            assert result == expected


class TestAutocompleteTermsResource:

    @patch.object(
        SearchTermService,
        "get_autocomplete_terms",
        lambda db, page: [
            make_search(123, type="Test Widget 1", value='idex'),
            make_search(456, type="Test Widget 2", value='dex'),
        ],
    )
    def test_get(self, client: FlaskClient):
        with client:
            results = client.get(f"/tokengallery/{BASE_ROUTE}/autocomplete-term/1", follow_redirects=True).get_json()
            expected = (
                SearchTermSchema(many=True)
                    .dump(
                    [
                        make_search(123, type="Test Widget 1", value='idex'),
                        make_search(456, type="Test Widget 2", value='dex'),
                    ]
                )
            )
            for r in results:
                assert r in expected
