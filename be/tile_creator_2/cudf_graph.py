import cugraph

from be.configuration import internal_id
from be.utils import timeit


class CudfGraph:

    @timeit("Constructing the GPU cuGraph object")
    def __init__(self, cudf_edgelist):
        self.graph = cugraph.Graph(directed=True)
        self.graph.from_cudf_edgelist(cudf_edgelist,
                                         source=internal_id("source"),
                                         destination= internal_id("target"),
                                         renumber=False)

    def get_vertexcount(self):
        return len(self.graph.nodes().to_pandas())