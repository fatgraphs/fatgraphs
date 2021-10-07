from typing import List

from mypy_extensions import TypedDict


class VertexInterface(TypedDict, total=False):
    graph_id: int
    vertex: str
    size: int
    pos: List[float]
