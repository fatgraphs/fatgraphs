from mypy_extensions import TypedDict

class SearchTermInterface(TypedDict, total=False):
    type: str
    value: str
