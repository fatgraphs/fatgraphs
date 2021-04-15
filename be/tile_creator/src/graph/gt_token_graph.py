import math

import numpy as np
from graph_tool import Graph
import pandas as pd

from be.configuration import MIN_MAX_PATH, CONFIGURATIONS
from be.tile_creator.src.graph.token_graph import TokenGraph


class GraphToolTokenGraph:
    '''
    This contains a token graph that is specifically used with the library graph_tool.
    An instacne of GraphToolTokenGraph contains all the static information needed to render a graph.
    '''

    def __init__(self, graph, configurations, metadata):
        if not isinstance(graph, TokenGraph):
            raise TypeError("GraphToolTokenGraph needs an instance of TokeGraph to be instantiated")
        self.metadata = metadata
        self.init_from_token_graph(graph, configurations)

    def init_from_token_graph(self, token_graph, configurations):
        # TODO: optimise

        self.g = Graph(directed=True)
        self.vertex_positions = self.g.new_vertex_property("vector<double>")
        self.edge_weight = self.g.new_edge_property("float")
        self.edge_length = self.g.new_edge_property("float")
        self.control_points = self.g.new_edge_property('vector<float>')
        self.vertices_size = self.g.new_vertex_property('float')

        # populate vertex positions with the positions specified i nt he layout
        for i, row in enumerate(token_graph.id_address_pos.sort_values("vertex")[["x", "y"]].values):
            self.vertex_positions[i] = row

        data = token_graph.edge_amounts.rename(columns={'source_id': 'source', 'target_id': 'target'})
        data['amount'] = pd.to_numeric(data['amount'])

        self.g.add_edge_list(
            data[["source", "target", "amount"]].values,
            hashed=False,
            eprops=[self.edge_weight])

        max_amount = float(self.edge_weight.a.max())
        self.edge_weight.a = list(
            map(
                lambda x: self._convert_amount_to_edge_width(x, max_amount),
                list(self.edge_weight.a)
            )
        )

        # TODO: loop edges have weigth zero, define a minimum
        edge_lengths = self._calculate_edge_lengths(data, token_graph.id_address_pos)

        self.edge_length.a = edge_lengths.values

        self._ensure_layout_is_square(token_graph)

        self.degree = self.g.degree_property_map("in")
        self.vertices_size.a = self.calculate_vertices_size(configurations)

        angle = configurations['edge_curvature']  # negative is clockwise
        for v in self.g.vertices():
            for e in v.out_edges():
                self.control_points[e] = [0, 0, 0.25, angle, 0.75, angle, 1, 0]

    def calculate_vertices_size(self, configuration_dictionary):

        med_distance = self.metadata.graph_metadata['median_pixel_distance'][0]
        targetMedian = med_distance * configuration_dictionary['target_median']
        targetMax = med_distance * configuration_dictionary['target_max']

        medToMax = max(list(self.degree.a)) - np.median(list(self.degree.a))
        targetMedToMax = targetMax - targetMedian
        degrees = (self.degree.a - np.median(self.degree.a)) * (targetMedToMax / medToMax) + targetMedian
        degrees = np.clip(degrees, 1, targetMax)
        return degrees

    def _convert_amount_to_edge_width(self, x, max_amount):
        # TODO: optimise
        zero_amount_become_one = x + 1.0
        log_amount = math.log10(zero_amount_become_one)
        min_thick = CONFIGURATIONS['min_edge_thickness']
        max_thick = CONFIGURATIONS['max_edge_thickness']
        thickness = (log_amount / math.log10(max_amount) * (max_thick - min_thick)) + min_thick
        return thickness

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

    def _ensure_layout_is_square(self, token_graph):
        # add two vertices that ensure that the layout is a square

        top_left = self.g.add_vertex()
        bottom_right = self.g.add_vertex()
        min_coordinate_value = self.metadata.graph_metadata['min'][0]
        max_coordinate_value = self.metadata.graph_metadata['max'][0]

        self.vertex_positions[top_left] = (min_coordinate_value, min_coordinate_value)
        self.vertex_positions[bottom_right] = (max_coordinate_value, max_coordinate_value)

        e1 = self.g.add_edge(top_left, top_left)
        e2 = self.g.add_edge(bottom_right, bottom_right)

        self.edge_weight[e1] = 10
        self.edge_weight[e2] = 10

        self.edge_length[e1] = 0
        self.edge_length[e2] = 0