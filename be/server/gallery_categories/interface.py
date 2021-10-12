from mypy_extensions import TypedDict


class GalleryCategoryInterface(TypedDict, total=False):

    id: int
    title: str
    description: str
    freetext: str
    urlslug: str