from typing import List
from .interface import GraphInterface
from .model import Graph
from .. import SessionLocal
from be.server import Base


class GraphService:

    @staticmethod
    def get_by_owner(owner: str, db) -> List[Graph]:
        graphs = db.query(Graph).filter_by(owner=owner).all()
        return graphs

    @staticmethod
    def get_by_id(graph_id: int, db) -> Graph:
       return db.query(Graph).get(graph_id)

    @staticmethod
    def get_by_name(graphName: str, db) -> Graph:
        return Graph.query.filter_by(graph_name=graphName).first()

    @staticmethod
    def get_by_owner_and_id(owner: str, graph_id: int, db) -> Graph:
        return Graph.query.filter_by(owner=owner, id=graph_id).first()

    @staticmethod
    def create(graph_to_create: GraphInterface, db):
        new_graph = Graph(
            tile_size=graph_to_create['tile_size'],
            max_transparency=graph_to_create['max_transparency'],
            median_pixel_distance=graph_to_create['median_pixel_distance'],
            max=graph_to_create['max'],
            vertices=graph_to_create['vertices'],
            bg_color=graph_to_create['bg_color'],
            med_vertex_size=graph_to_create['med_vertex_size'],
            max_vertex_size=graph_to_create['max_vertex_size'],
            curvature=graph_to_create['curvature'],
            min_transparency=graph_to_create['min_transparency'],
            owner=graph_to_create['owner'],
            source=graph_to_create['source'],
            edges=graph_to_create['edges'],
            std_transparency_as_percentage=graph_to_create['std_transparency_as_percentage'],
            min=graph_to_create['min'],
            zoom_levels=graph_to_create['zoom_levels'],
            output_folder=graph_to_create['output_folder'],
            tile_based_mean_transparency=graph_to_create['tile_based_mean_transparency'],
            med_edge_thickness=graph_to_create['med_edge_thickness'],
            graph_name=graph_to_create['graph_name'],
            max_edge_thickness=graph_to_create['max_edge_thickness'],
            labels=graph_to_create['labels'])

        db.add(new_graph)
        db.commit()
        db.flush()
        # db.refresh(new_graph)
        return new_graph

    @staticmethod
    def update(graph: Graph, changes: GraphInterface, db: object):
        update = graph.update(changes)
        db.commit()
        return update
