from typing import List
from .interface import GraphInterface
from .model import Graph

class GraphService:

    @staticmethod
    def get_all(db) -> List[Graph]:
        graphs = db.query(Graph).all()
        return graphs

    @staticmethod
    def get_by_id(graph_id: int, db) -> Graph:
        return db.query(Graph).get(graph_id)

    @staticmethod
    def create(graph_to_create: GraphInterface, db):
        assert 'gallery_categories' in db.bind.engine.table_names()
        new_graph = Graph(
            graph_name=graph_to_create['graph_name'],
            graph_category=int(graph_to_create['graph_category']),
            vertices=graph_to_create['vertices'],
            edges=graph_to_create['edges'],
        )
        db.add(new_graph)
        db.commit()
        db.flush()
        return new_graph

    @staticmethod
    def update(graph: Graph, changes: GraphInterface, db: object):
        update = graph.update(changes)
        db.commit()
        return update

    @staticmethod
    def get_by_type(gallery_type, db):
        return db.query(Graph).filter_by(graph_category=gallery_type).all()