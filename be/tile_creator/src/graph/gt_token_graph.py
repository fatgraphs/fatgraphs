import math

import numpy as np
from graph_tool import Graph
import pandas as pd

from be.configuration import MIN_MAX_PATH, CONFIGURATIONS
from be.tile_creator.src.graph.token_graph import TokenGraph
from be.utils import shift_and_scale


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


        self.edge_weight.a = self.calculate_edges_thickness(configurations)

        # TODO: loop edges have weigth zero, define a minimum
        edge_lengths = self._calculate_edge_lengths(data, token_graph.id_address_pos)

        self.edge_length.a = edge_lengths.values

        self._ensure_layout_is_square(token_graph)

        self.degree = self.g.degree_property_map("in")
        self.vertices_size.a = self.calculate_vertices_size(configurations)

        for v in self.g.vertices():
            for e in v.out_edges():
                curvature = max(1, self.edge_length[e] / max(1, self.metadata.graph_metadata['median_pixel_distance'][0]))
                arbitrarily_scaled_curvature = max(1, curvature * 0.75)
                # exp = math.log10(self.edge_length[e] + 1)
                self.control_points[e] = [0, 0, 0.25, curvature, 0.75, curvature, 1, 0]

    def calculate_vertices_size(self, configuration_dictionary):

        med_distance = self.metadata.graph_metadata['median_pixel_distance'][0]
        target_median = med_distance * configuration_dictionary['med_vertex_size']
        target_max = med_distance * configuration_dictionary['max_vertex_size']

        return shift_and_scale(self.degree.a, target_median, target_max)


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

        self.edge_weight[e1] = 1
        self.edge_weight[e2] = 1

        self.edge_length[e1] = 1
        self.edge_length[e2] = 1

    def calculate_edges_thickness(self, configurations):
        med_distance = self.metadata.graph_metadata['median_pixel_distance'][0]
        target_median = med_distance * configurations['med_edge_thickness']
        target_max = med_distance * configurations['max_edge_thickness']

        log_amounts = np.log10(self.edge_weight.a + 1) # amounts can be huge numbers, reduce the range
        return shift_and_scale(log_amounts, target_median, target_max)