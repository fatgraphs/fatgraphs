from app import db
from typing import List
from .model import Vertex
from ..metadata.service import MetadataService


class VertexService:

    @staticmethod
    def get_closest(graph_name: str, x: float, y: float) -> Vertex:
        closest = Vertex.getClosest(graph_name, x, y)
        return closest

    @staticmethod
    def get_matching(graph_name: str, meta_type: str, meta_value: str) -> List[Vertex]:
        matches = MetadataService.get_by_type_and_value(meta_type, meta_value)
        eths = list(map(lambda e: e.eth_source, matches))
        # TODO USE GRAPH NAME
        by_eths = VertexService.get_by_eths(eths)
        return by_eths

    @staticmethod
    def get_by_eths(eths: List[str]) -> List[Vertex]:
        closest = Vertex.query.filter(Vertex.eth.in_(eths)).all()
        return closest
