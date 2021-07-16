from mypy_extensions import TypedDict


class MetadataInterface(TypedDict, total=False):
    id: int
    eth_target: str
    eth_source: str
    meta_type: str
    meta_value: str
    entity: str