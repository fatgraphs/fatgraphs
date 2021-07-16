from typing import List
from app import db
from .interface import GraphInterface
from .model import Graph
from ..metadata import Metadata


class GraphService:

    @staticmethod
    def get_by_owner(owner: str) -> List[Graph]:
        return Graph.query.filter_by(owner=owner).all()

    @staticmethod
    def get_by_name(graphName: str) -> Graph:
        return Graph.query.filter_by(graph_name=graphName).first()

    @staticmethod
    def create(graph_to_create: GraphInterface):
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

        db.session.add(new_graph)
        db.session.commit()
        return new_graph
