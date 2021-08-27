from be.tile_creator.src.new_way.datasource import DataSource
from be.tile_creator.src.new_way.test.fixtures_vertex import *
from be.tile_creator.src.new_way.test.fixtures import *
from be.tile_creator.src.new_way.test.fixtures_graph import *
from be.tile_creator.src.new_way.test.fixtures_edge import *

class TestRawdata:

    def test_not_none(self, csv_path):
        assert csv_path is not None
        raw_data = DataSource(csv_path)
        assert raw_data is not None


