from unittest.mock import patch

from flask.testing import FlaskClient

from . import BASE_ROUTE, Graph, GraphSchema
from .service import GraphService
from ..test.fixtures import client, app  # noqa


def make_graph(
    id: int = 123, name: str = "Test widget"
) -> Graph:
    return Graph(id=id, graph_name=name)


class TestGraphResource:
    @patch.object(
        GraphService,
        "get_all",
        lambda db : [
            make_graph(123, name="Test Widget 1"),
            make_graph(456, name="Test Widget 2"),
        ],
    )
    def test_get(self, client: FlaskClient):
        with client:
            results = client.get(f"/tokengallery/{BASE_ROUTE}", follow_redirects=True).get_json()
            expected = (
                GraphSchema(many=True)
                .dump(
                    [
                        make_graph(123, name="Test Widget 1"),
                        make_graph(456, name="Test Widget 2"),
                    ]
                )
                
            )
            for r in results:
                assert r in expected