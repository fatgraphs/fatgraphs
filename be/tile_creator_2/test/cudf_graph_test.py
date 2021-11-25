from be.tile_creator_2.edge_data import EdgeData
from .fixtures_edge import *  # noqa

class TestCudfGraph:

    def test_graph(self, edge_data_with_edges: EdgeData):
        graph = CudfGraph(edge_data_with_edges.cudf_frame)

        assert len(graph.graph.edges().to_pandas()) == \
               len(edge_data_with_edges.cudf_frame)
