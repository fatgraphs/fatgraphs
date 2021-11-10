from mypy_extensions import TypedDict


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
