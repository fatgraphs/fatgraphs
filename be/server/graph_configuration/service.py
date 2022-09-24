from .interface import GraphConfigurationInterface
from .model import Graph, GraphConfiguration


class GraphConfigurationService:

    @staticmethod
    def get_by_id(graph_id: int, db) -> Graph:
        return db.query(GraphConfiguration).filter_by(graph=graph_id).first()

    @staticmethod
    def create(graph_to_create: GraphConfigurationInterface, db):
        assert 'tg_graph_configs' in db.bind.engine.table_names()
        new_graph_configuration = GraphConfiguration(
            tile_size=graph_to_create['tile_size'],
            zoom_levels=graph_to_create['zoom_levels'],
            min_transparency=graph_to_create['min_transparency'],
            max_transparency=graph_to_create['max_transparency'],
            tile_based_mean_transparency=graph_to_create['tile_based_mean_transparency'],
            std_transparency_as_percentage=graph_to_create['std_transparency_as_percentage'],
            max_edge_thickness=graph_to_create['max_edge_thickness'],
            med_edge_thickness=graph_to_create['med_edge_thickness'],
            max_vertex_size=graph_to_create['max_vertex_size'],
            med_vertex_size=graph_to_create['med_vertex_size'],
            curvature=graph_to_create['curvature'],
            bg_color=graph_to_create['bg_color'],
            source=graph_to_create['source'],
            median_pixel_distance=float(graph_to_create['median_pixel_distance']),
            min=float(graph_to_create['min']),
            max=float(graph_to_create['max']),
            graph=int(graph_to_create['graph']),
        )

        db.add(new_graph_configuration)
        db.commit()
        db.flush()
        return new_graph_configuration
