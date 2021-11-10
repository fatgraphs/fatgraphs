from mypy_extensions import TypedDict


class GraphInterface(TypedDict, total=False):

    id: int
    graph_name: str
    graph_category: int
    vertices: int
    edges: int
