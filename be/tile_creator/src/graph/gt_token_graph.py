from graph_tool import Graph
import pandas as pd
from be.tile_creator.src.graph.token_graph import TokenGraph


class GraphToolTokenGraph:
    '''
    This contains a token graph that is specifically used with the library graph_tool.
    An instacne of GraphToolTokenGraph contains all the static information needed to render a graph.
    '''

    def __init__(self, edge_ids_to_amount, visual_layout, metadata, edge_curvature):
        self.metadata = metadata
        self.edge_curvature = edge_curvature if edge_curvature < 0 else -1 * edge_curvature
        self.g = Graph(directed=True)
        self._add_edges(edge_ids_to_amount)
        self.vertex_positions = self.g.new_vertex_property("vector<float>",
                                                      vals=visual_layout.vertex_positions[["x", "y"]].values)
        self.edge_length = self.g.new_edge_property("float", vals=visual_layout.edge_lengths)
        self.vertex_sizes = self.g.new_vertex_property('float', vals=visual_layout.vertex_sizes)
        self.vertex_shapes = self.g.new_vertex_property('string', vals=visual_layout.vertex_shapes)
        self.edge_thickness = self.g.new_edge_property("float", vals=visual_layout.edge_thickness)
        self._make_bezier_points()
        # edge transparency needs to be populated at run-time
        self.edge_transparencies = []
        for zl in range(0, metadata.graph_metadata.zoom_levels[0]):
            self.edge_transparencies.append(self.g.new_edge_property("vector<float>"))

    def _make_bezier_points(self):
        self.control_points = self.g.new_edge_property('vector<float>')
        for v in self.g.vertices():
            for e in v.out_edges():
                curvature = self.edge_length[e] * self.edge_curvature
                self.control_points[e] = [0, 0, 0.25, curvature, 0.75, curvature, 1, 0]

    def _add_edges(self, edge_ids_to_amount):
        data = edge_ids_to_amount.rename(columns={'source_id': 'source', 'target_id': 'target'})
        # hashed = False ensure that vertex values correspond to vertex indices
        self.g.add_edge_list(
            data[["source", "target"]].values,
            hashed=False)
