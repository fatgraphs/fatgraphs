from be.tile_creator.src.new_way.cudf_graph import CudfGraph
from be.tile_creator.src.new_way.edge_data import EdgeData
from be.tile_creator.src.new_way.test.fixtures_vertex import *
from be.tile_creator.src.new_way.test.fixtures import *
from be.tile_creator.src.new_way.test.fixtures_graph import *
from be.tile_creator.src.new_way.test.fixtures_edge import *

class TestCudfGraph:

    def test_graph(self, edge_data_with_edges: EdgeData):
        graph = CudfGraph(edge_data_with_edges.get_source_target_amount())

        assert len(graph.get_graph().edges().to_pandas()) == \
               len(edge_data_with_edges.get_source_target_amount())


