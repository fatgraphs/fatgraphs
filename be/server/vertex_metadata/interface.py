from mypy_extensions import TypedDict


class VertexMetadataInterface(TypedDict, total=False):
    id: int
    vertex: str
    type: str
    value: str
    account_type: int
    description: str