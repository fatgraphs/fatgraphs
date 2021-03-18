# TODO: rename and include max, min, width and height information here as graph property (to avoid
# having to pass to render 2 object)
class GraphRenderingInfo:

    def __init__(self, g, vertex_positions, deg, edge_weight, edge_length):
        self.g = g
        self.vertex_positions = vertex_positions
        self.deg = deg
        self.edge_weight = edge_weight
        self.edge_length = edge_length