from mypy_extensions import TypedDict

from be.tile_creator_2.graph_data import GraphData


class GraphInterface(TypedDict, total=False):
    id: int
    graph_name: str
    graph_category: int
    vertices: int
    edges: int

    @staticmethod
    def from_graph_data(graph_data: GraphData):
        result = GraphInterface(graph_name=graph_data.graph_name,
                                graph_category=graph_data.graph_category,
                                vertices=graph_data.vertex_count,
                                edges=graph_data.vertex_count)
        return result
