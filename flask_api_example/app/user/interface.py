from mypy_extensions import TypedDict
from typing import List


class UserInterface(TypedDict, total=False):
    name: str
    recent_metadata_searches: List[str]
