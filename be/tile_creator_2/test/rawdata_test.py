from be.tile_creator_2.datasource import DataSource
from .fixtures import *  # noqa

class TestRawdata:

    def test_not_none(self, csv_path):
        assert csv_path is not None
        raw_data = DataSource(csv_path)
        assert raw_data is not None


