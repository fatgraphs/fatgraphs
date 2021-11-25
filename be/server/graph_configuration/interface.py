from mypy_extensions import TypedDict

from be.tile_creator_2.graph_data import GraphData
from be.tile_creator_2.gtm_args import GtmArgs


class GraphConfigurationInterface(TypedDict, total=False):
    id: int
    tile_size: str
    zoom_levels: int
    min_transparency: float
    max_transparency: float
    tile_based_mean_transparency: float
    std_transparency_as_percentage: float
    max_edge_thickness: float
    med_edge_thickness: float
    max_vertex_size: float
    med_vertex_size: float
    curvature: float
    bg_color: str
    source: str
    median_pixel_distance: float
    min: float
    max: float
    graph: int

    @staticmethod
    def from_gtm_args(gtm_args: GtmArgs, graph_id: int, graph_data: GraphData):
        result = GraphConfigurationInterface(
            tile_size=gtm_args.get_tile_size(),
            zoom_levels=gtm_args.get_zoom_levels(),
            min_transparency=gtm_args.get_min_transparency(),
            max_transparency=gtm_args.get_max_transparency(),
            tile_based_mean_transparency=gtm_args.get_tile_based_mean_transparency(),
            std_transparency_as_percentage=gtm_args.get_std_percentage(),
            max_edge_thickness=gtm_args.get_max_edge_thickness(),
            med_edge_thickness=gtm_args.get_median_edge_thickness(),
            max_vertex_size=gtm_args.get_max_vertex_size(),
            med_vertex_size=gtm_args.get_med_vertex_size(),
            curvature=gtm_args.get_curvature(),
            bg_color=gtm_args.get_bg_color(),
            source=gtm_args.get_source_file(),

            #TODo remove
            median_pixel_distance=graph_data.median_pixel_distance,
            min=graph_data.graph_space_bound.get_min_coord(),
            max=graph_data.graph_space_bound.get_max_coord(),

            graph=graph_id
        )
        return result
