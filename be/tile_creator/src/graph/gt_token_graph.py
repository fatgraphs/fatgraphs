from graph_tool import Graph
import pandas as pd
from be.tile_creator.src.graph.token_graph import TokenGraph


class GraphToolTokenGraph:
    '''
    This contains a token graph that is specifically used with the library graph_tool.
    An instacne of GraphToolTokenGraph contains all the static information needed to render a graph.
    '''

    def __init__(self, graph, visual_layout, metadata, edge_curvature):
        if not isinstance(graph, TokenGraph):
            raise TypeError("GraphToolTokenGraph needs an instance of TokeGraph to be instantiated")
        self.metadata = metadata
        self.edge_curvature = edge_curvature if edge_curvature < 0 else -1 * edge_curvature
        self.g = Graph(directed=True)
        self._add_edges(graph)
        self.vertex_positions = self._make_vertex_positions(visual_layout)
        self.edge_length = self.g.new_edge_property("float", vals=visual_layout.edge_lengths_graph_space)
        self.vertex_sizes = self.g.new_vertex_property('float', vals=visual_layout.vertex_sizes)
        self.edge_thickness = self.g.new_edge_property("float", vals=visual_layout.edge_thickness)
        self._make_bezier_points()
        self.edge_transparencies = self.g.new_edge_property("vector<float>")

    def _make_bezier_points(self):
        self.control_points = self.g.new_edge_property('vector<float>')
        for v in self.g.vertices():
            for e in v.out_edges():
                curvature = self.edge_length[e] * self.edge_curvature
                self.control_points[e] = [0, 0, 0.25, curvature, 0.75, curvature, 1, 0]

    def _add_edges(self, graph):
        data = graph.ids_to_amount.rename(columns={'source_id': 'source', 'target_id': 'target'})
        # hashed = False ensure that vertex values correspond to vertex indices
        self.g.add_edge_list(
            data[["source", "target"]].values,
            hashed=False)

    def _make_vertex_positions(self, visual_layout):
        # vertex_positions = self.g.new_vertex_property("vector<float>")
        vertex_positions = self.g.new_vertex_property("vector<float>",
                                                      vals=visual_layout.vertex_positions.sort_values('vertex')[
                                                          ["x", "y"]].values)
        # populate vertex positions with the positions specified i nt he layout
        # for i, row in enumerate(visual_layout.vertex_positions.sort_values('vertex')[["x", "y"]].values):
        #     vertex_positions[i] = row
        return vertex_positions
