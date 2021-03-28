import math

import numpy as np
from graph_tool import Graph
import pandas as pd

from be.tile_creator.src.graph.token_graph import TokenGraph


class GraphToolTokenGraph:
    '''
    This contains a token graph that is specifically used with the library graph_tool.
    An instacne of GraphToolTokenGraph contains all the static information needed to render a graph.
    '''

    def __init__(self, graph):
        if not isinstance(graph, TokenGraph):
            raise TypeError("GraphToolTokenGraph needs an instance of TokeGraph as argument")
        self.init_from_token_graph(graph)

    def init_from_token_graph(self, token_graph):
        # TODO: optimise

        self.g = Graph(directed=True)
        self.vertex_positions = self.g.new_vertex_property("vector<double>")
        self.edge_weight = self.g.new_edge_property("float")
        self.edge_length = self.g.new_edge_property("float")

        # populate vertex positions with the positions specified i nt he layout
        for i, row in enumerate(token_graph.ids_to_positions.sort_values("vertex")[["x", "y"]].values):
            self.vertex_positions[i] = row

        data = token_graph.edge_ids_amounts.rename(columns={'source_id': 'source', 'target_id': 'target'})
        data['amount'] = pd.to_numeric(data['amount'])

        self.g.add_edge_list(
            data[["source", "target", "amount"]].values,
            hashed=False,
            eprops=[self.edge_weight])

        self.edge_weight.a = list(map(lambda x: (math.log10(x + 1.0) + 1.0) * 0.8, list(self.edge_weight.a)))

        # TODO: loop edges have weigth zero, define a minimum
        edge_lengths = self._calculate_edge_lengths(data, token_graph.ids_to_positions)

        self.edge_length.a = edge_lengths.values

        self._square_out(token_graph.ids_to_positions)

        self.degree = self.g.degree_property_map("in")
        self.degree.a = 4 * (np.sqrt(self.degree.a) * 0.5 + 0.4)

    def _calculate_edge_lengths(self, data, layout):
        data = data.merge(layout.rename(columns={"vertex": "target"}), on='target', how='left') \
            .rename(columns={'x': 't_x', 'y': 't_y'})
        data = data.merge(layout.rename(columns={"vertex": "source"}), on='source', how='left') \
            .rename(columns={'x': 's_x', 'y': 's_y'})
        delta_x = - data['t_x'] + data['s_x']
        delta_y = - data['t_y'] + data['s_y']
        ssx = delta_x ** 2
        ssy = delta_y ** 2
        ssx_ssy = ssx + ssy
        ssy___ = ssx_ssy ** 0.5
        return ssy___

    def _square_out(self, values):
        # add two vertices that ensure that the layout is a square
        temp_max_x = values['x'].max()
        temp_max_y = values['y'].max()
        temp_min_x = values['x'].min()
        temp_min_y = values['y'].min()

        top_left = self.g.add_vertex()
        bottom_right = self.g.add_vertex()
        min_coordinate_value = min(temp_min_x, temp_min_y)
        max_coordinate_value = max(temp_max_x, temp_max_y)

        self.vertex_positions[top_left] = (min_coordinate_value, min_coordinate_value)
        self.vertex_positions[bottom_right] = (max_coordinate_value, max_coordinate_value)

        e1 = self.g.add_edge(top_left, top_left)
        e2 = self.g.add_edge(bottom_right, bottom_right)

        self.edge_weight[e1] = 10
        self.edge_weight[e2] = 10

        self.edge_length[e1] = 0
        self.edge_length[e2] = 0

        self.max_x = max_coordinate_value
        self.max_y = max_coordinate_value
        self.min_x = min_coordinate_value
        self.min_y = min_coordinate_value
        self.side = max_coordinate_value - min_coordinate_value
