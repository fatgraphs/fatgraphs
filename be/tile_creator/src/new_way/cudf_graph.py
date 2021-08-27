import cugraph

from be.configuration import internal_id


class CudfGraph:

    def __init__(self, cudf_edgelist):
        self._graph = cugraph.Graph(directed=True)
        self._graph.from_cudf_edgelist(cudf_edgelist,
                                         source=internal_id("source"),
                                         destination= internal_id("target"),
                                         renumber=False)

    def get_graph(self):
        return self._graph

    def get_vertexcount(self):
        return len(self._graph.nodes().to_pandas())