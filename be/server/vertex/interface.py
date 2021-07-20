from typing import List

from mypy_extensions import TypedDict


class VertexInterface(TypedDict, total=False):
    id: int
    graph_id: int
    eth: str
    size: int
    pos: List[float]
