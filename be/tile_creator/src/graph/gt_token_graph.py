import math
import numpy as np
from graph_tool import Graph

from be.tile_creator.src.graph.token_graph import TokenGraph


class GraphToolTokenGraph:
    '''
    This contains a token graph that is specifically used with the library graph tool.
    An instacne of GraphToolTokenGraph contains all the static information needed to render a graph.
    '''

    def __init__(self, graph):
        if not isinstance(graph, TokenGraph):
            raise TypeError("GraphToolTokenGraph needs an instance of TokeGraph as argument")
        self.g = None
        self.vertex_positions = None
        self.degree = None
        self.edge_weight = None
        self.edge_length = None
        self.max_x = None
        self.max_y = None
        self.min_x = None
        self.min_y = None
        self.side = None
        self.init_from_token_graph(graph)

    def init_from_token_graph(self, token_graph):
        # TODO: optimise

        self.g = Graph(directed=True)
        self.vertex_positions = self.g.new_vertex_property("vector<double>")
        self.edge_weight = self.g.new_edge_property("float")
        self.edge_length = self.g.new_edge_property("double")

        values = token_graph.layout.sort_values(by=['vertex'])
        self._square_out(self.vertex_positions, values)

        # populate vertex positions with the positions specified i nt he layout
        for i, v in values.iterrows():
            self.vertex_positions[i] = (v['x'], v['y'])

        for index, e in token_graph.edge_ids_amounts.iterrows():
            s = e['source_id']
            d = e['target_id']
            edge = self.g.add_edge(s, d)

            self.edge_weight[edge] = (math.log10(float(e['amount']) + 1.0) + 1.0) / 10.0

            distance_between_vertices = math.dist(self.vertex_positions[int(s)], self.vertex_positions[int(d)])
            self.edge_length[edge] = distance_between_vertices

        self.degree = self.g.degree_property_map("in")
        self.degree.a = 4 * (np.sqrt(self.degree.a) * 0.1 + 0.4)

    def _square_out(self, vertex_positions, values):
        # add two vertices that ensure that the layout is a square
        max_x = values['x'].max()
        max_y = values['y'].max()
        min_x = values['x'].min()
        min_y = values['y'].min()
        top_left = self.g.add_vertex()
        bottom_right = self.g.add_vertex()
        min_coordinate_value = min(min_x, min_y)
        max_coordinate_value = max(max_x, max_y)
        vertex_positions[top_left] = (min_coordinate_value, min_coordinate_value)
        vertex_positions[bottom_right] = (max_coordinate_value, max_coordinate_value)
        self.g.add_edge(top_left, top_left)
        self.g.add_edge(bottom_right, bottom_right)
        self.max_x = max_coordinate_value
        self.max_y = max_coordinate_value
        self.min_x = min_coordinate_value
        self.min_y = min_coordinate_value
        self.side = max_x - min_x