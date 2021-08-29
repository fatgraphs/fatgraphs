from random import random
from unittest.mock import patch
from flask.testing import FlaskClient

from .service import  VertexMetadataService
from .vertex_fixtures import vertex_metedata_1, vertex_metedata_2, vertex_metadata_1_param
from ..test.fixtures import client, app  # noqa


from . import BASE_ROUTE, VertexMetadata, VertexMetadataSchema


class TestGraphResource:
    @patch.object(
        VertexMetadataService,
        "get_by_eth",
        lambda eth, db : [
            vertex_metedata_1
        ],
    )
    def test_get(self, client: FlaskClient):
        with client:
            results = client.get(f"/tokengallery/{BASE_ROUTE}/vertex/test_eth", follow_redirects=True).get_json()
            expected = (
                VertexMetadataSchema(many=True)
                .dump(
                    [
                        vertex_metedata_1
                    ]
                )
                
            )
            assert len(results) == 1
            for r in results:
                assert r in expected

    @patch.object(
                VertexMetadataService, "create", lambda metadata_to_insert, db: VertexMetadata(**metadata_to_insert)
            )
    def test_post(self, client: FlaskClient, vertex_metadata_1_param):  # noqa
        with client:

            params = {**vertex_metadata_1_param}
            params.pop('account_type')
            params['accountType'] = vertex_metadata_1_param['account_type']
            result = client.post(f"/tokengallery/{BASE_ROUTE}/create", json=params).get_json()

            expected = (
                VertexMetadataSchema()
                .dump(VertexMetadata(**vertex_metadata_1_param))

            )
            assert result == expected
