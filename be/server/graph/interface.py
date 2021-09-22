from mypy_extensions import TypedDict


class GraphInterface(TypedDict, total=False):

    tile_size: str
    max_transparency: float
    median_pixel_distance: float
    max: float
    vertices: int
    bg_color: str
    med_vertex_size: float
    max_vertex_size: float
    curvature: float
    min_transparency: float
    source: str
    edges: int
    std_transparency_as_percentage: float
    min: float
    zoom_levels: int
    tile_based_mean_transparency: float
    med_edge_thickness: float
    id: int
    graph_name: str
    max_edge_thickness: float