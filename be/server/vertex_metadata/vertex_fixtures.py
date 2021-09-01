from copy import deepcopy
import pytest
from be.server.vertex_metadata import VertexMetadata
from be.server.vertex_metadata.interface import VertexMetadataInterface


@pytest.fixture
def vertex_metadata_1_param():
    yield dict(id=1,
                vertex='test_eth',
                type='test_type',
                label='test_label',
                account_type=0,
                description='test_description')


@pytest.fixture
def vertex_metedata_1(vertex_metadata_1_param: VertexMetadataInterface):
    yield VertexMetadata(**vertex_metadata_1_param)

@pytest.fixture
def vertex_metedata_1_different_id(vertex_metadata_1_param: VertexMetadataInterface):
    new_params = deepcopy(vertex_metadata_1_param)
    new_params['id'] = 123456789
    yield VertexMetadata(**new_params)


@pytest.fixture
def vertex_metadata_2_param():
    yield dict(id=2,
                vertex='test_eth_2',
                type='test_type_2',
                label='test_label_2',
                account_type=0,
                description='test_description_2')


@pytest.fixture
def vertex_metedata_2(vertex_metadata_2_param: VertexMetadataInterface):
    yield VertexMetadata(**vertex_metadata_2_param)
