from typing import List
from .interface import GraphInterface
from .model import Graph
from ..vertex import Vertex


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
        new_graph = Graph(
            output_folder='',
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
            source=graph_to_create['source'],
            edges=graph_to_create['edges'],
            std_transparency_as_percentage=graph_to_create['std_transparency_as_percentage'],
            min=graph_to_create['min'],
            zoom_levels=graph_to_create['zoom_levels'],
            tile_based_mean_transparency=graph_to_create['tile_based_mean_transparency'],
            med_edge_thickness=graph_to_create['med_edge_thickness'],
            graph_name=graph_to_create['graph_name'],
            max_edge_thickness=graph_to_create['max_edge_thickness']
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
    def get_vertex_table_name(graph_id: int, db) -> str:
        graph = GraphService.get_by_id(graph_id, db)
        return graph.graph_name + '_' + str(graph.id)
