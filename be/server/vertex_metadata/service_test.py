from typing import List
from . import VertexMetadata
from .interface import VertexMetadataInterface
from .service import VertexMetadataService
from .vertex_fixtures import vertex_metedata_2, vertex_metedata_1, vertex_metadata_1_param, vertex_metadata_2_param, vertex_metedata_1_different_id
from ..test.fixtures import app, db, assert_lists_equal

def test_get_by_eth(db: object, vertex_metedata_1: VertexMetadata, vertex_metedata_2: VertexMetadata):

    def assert_get_by_eth(expected: List[VertexMetadata], query_eth):
        results: List[VertexMetadata] = VertexMetadataService.get_by_eth(query_eth, db)
        assert_lists_equal(expected, results)

    db.add(vertex_metedata_1)
    db.add(vertex_metedata_2)
    db.commit()

    assert_get_by_eth([vertex_metedata_1], vertex_metedata_1.eth)
    assert_get_by_eth([vertex_metedata_2], vertex_metedata_2.eth)
    assert_get_by_eth([], 'eth_not_present')

def test_get_by_label(db: object, vertex_metedata_1: VertexMetadata, vertex_metedata_2: VertexMetadata):

    def assert_get_by_label(expected: List[VertexMetadata], query_label):
        results: List[VertexMetadata] = VertexMetadataService.get_by_label(query_label, db)
        assert_lists_equal(expected, results)

    db.add(vertex_metedata_1)
    db.add(vertex_metedata_2)
    db.commit()

    assert_get_by_label([vertex_metedata_1], vertex_metedata_1.label)
    assert_get_by_label([vertex_metedata_2], vertex_metedata_2.label)
    assert_get_by_label([], 'label_not_present')

def test_get_by_type(db: object, vertex_metedata_1: VertexMetadata, vertex_metedata_2: VertexMetadata):

    def assert_get_by_type(expected: List[VertexMetadata], query_type):
        results: List[VertexMetadata] = VertexMetadataService.get_by_type(query_type, db)
        assert_lists_equal(expected, results)

    db.add(vertex_metedata_1)
    db.add(vertex_metedata_2)
    db.commit()

    assert_get_by_type([vertex_metedata_1], vertex_metedata_1.type)
    assert_get_by_type([vertex_metedata_2], vertex_metedata_2.type)
    assert_get_by_type([], 'type_not_present')


def test_create(db: object, vertex_metadata_1_param: VertexMetadataInterface):

    def assert_db_empty():
        by_eth = VertexMetadataService.get_by_eth(vertex_metadata_1_param['eth'], db)
        by_label = VertexMetadataService.get_by_label(vertex_metadata_1_param['label'], db)
        by_type = VertexMetadataService.get_by_type(vertex_metadata_1_param['type'], db)
        assert len(by_eth) == len(by_type) == len(by_label) == 0

    assert_db_empty()

    VertexMetadataService.create(vertex_metadata_1_param, db)

    by_eth = VertexMetadataService.get_by_eth(vertex_metadata_1_param['eth'], db)
    by_label = VertexMetadataService.get_by_label(vertex_metadata_1_param['label'], db)
    by_type = VertexMetadataService.get_by_type(vertex_metadata_1_param['type'], db)

    assert len(by_eth) == len(by_type) == len(by_label)
    assert by_eth[0] == by_type[0] == by_label[0]


def test_get_unique_types(db: object, vertex_metedata_1_different_id: VertexMetadata, vertex_metedata_1: VertexMetadata):
    db.add(vertex_metedata_1_different_id)
    db.add(vertex_metedata_1)
    db.commit()
    unique_types = VertexMetadataService.get_unique_types(1, db)
    assert len(unique_types) == 1
    assert vertex_metedata_1.type in unique_types

    db.add(VertexMetadata(id=1234, type="something new"))
    db.commit()

    unique_types = VertexMetadataService.get_unique_types(1, db)
    assert len(unique_types) == 2

def test_get_unique_labels(db: object, vertex_metedata_1_different_id: VertexMetadata, vertex_metedata_1: VertexMetadata):
    db.add(vertex_metedata_1_different_id)
    db.add(vertex_metedata_1)
    db.commit()
    unique_labels = VertexMetadataService.get_unique_labels(1, db)
    assert len(unique_labels) == 1
    assert vertex_metedata_1.label in unique_labels

    db.add(VertexMetadata(id=1234, type="something new"))
    db.commit()

    unique_labels = VertexMetadataService.get_unique_labels(1, db)
    assert len(unique_labels) == 2
