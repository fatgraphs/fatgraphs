import math

import cudf
import cugraph
import pandas as pd
from graph_tool.all import Graph
import numpy as np

from be.tile_creator.src.graph.gt_token_graph import GraphRenderingInfo
from be.tile_creator.src.layout.layout_generator import LayoutGenerator


class TokenGraph:

    def __init__(self, path, options):
        self.raw_data = pd.read_csv(path, **options)
        self.addresses_to_ids = self._map_addresses_to_ids()
        self.gpu_frame = self._make_graph_gpu_frame(self.addresses_to_ids)
        lg = LayoutGenerator()
        self.layout = lg.make_layout(self.gpu_frame)
        # TODO: move graph_tool_graph out; make it independent and self contained for rendering
        self.graph_tool = self.convert_to_graph_tool_graph()

    def _map_addresses_to_ids(self):
        data = self.raw_data
        # get unique addresses
        column_values = data[["source", "target"]].values.ravel()
        unique_values = pd.unique(column_values)
        # indices to vertices
        mapping = pd.DataFrame(unique_values).reset_index().rename(columns={"index": "vertex", 0: "address"})
        return mapping

    def _make_graph_gpu_frame(self, addresses_to_ids):
        data = self.raw_data

        # associate source id to the source address
        data = data.merge(addresses_to_ids.rename(columns={"address": "source"})).rename(
            columns={"vertex": "source_id"})

        # associate target_id with target address
        data = data.merge(addresses_to_ids.rename(columns={"address": "target"})).rename(
            columns={"vertex": "target_id"})

        self.edge_ids_amounts = data[["source_id", "target_id", "amount"]]

        data_ids = data[["source_id", "target_id"]]

        data_ids = cudf.DataFrame.from_pandas(data_ids)
        graph = cugraph.Graph()
        graph.from_cudf_edgelist(data_ids, source='source_id', destination='target_id')
        return graph

    def convert_to_graph_tool_graph(self):
        # TODO: optimise: does around 2600 edges every 10 seconds currently

        g = Graph(directed=True)
        vertex_positions = g.new_vertex_property("vector<double>")
        edge_weight = g.new_edge_property("float")
        edge_length = g.new_edge_property("double")
        # time1= []
        # time2= []
        # time3= []
        values = self.layout.vertex_id_to_xy_tuple.sort_values(by=['vertex'])

        # t01 = time.time_ns()
        for i, v in values.iterrows():
            vertex_positions[i] = (v['x'], v['y'])

        # t02 = time.time_ns()
        # print("Initial loop took: " + str(t02 - t01))

        for index, e in self.edge_ids_amounts.iterrows():
            # t0 = time.time_ns()
            s = e['source_id']
            d = e['target_id']
            edge = g.add_edge(s, d)
            # t1 = time.time_ns()
            # time1.append(t1 - t0)

            # amounts have high range, to avoid extra-large edges we log it
            # t2 = time.time_ns()
            # time2.append(t2 - t1)
            try:
                edge_weight[edge] = (math.log10(float(e['amount']) + 1.0) + 1.0) / 10.0
            except Exception:
                print("hhh")
            distance_between_vertices = math.dist(vertex_positions[int(s)], vertex_positions[int(d)])
            edge_length[edge] = distance_between_vertices
            # t3 = time.time_ns()
            # time3.append(t3 - t2)


        # print("_________")
        # print(np.mean(time1))
        # print(np.mean(time2))
        # print(np.mean(time3))
        # print("normal technique took: " + str(int(reduce(lambda a, b: a + b, time2))))
        top_left = g.add_vertex()
        bottom_right = g.add_vertex()
        min_coordinate_value = min(self.layout.min_x, self.layout.min_y)
        max_coordinate_value = min(self.layout.max_x, self.layout.max_y)
        vertex_positions[top_left] = (min_coordinate_value, min_coordinate_value)
        vertex_positions[bottom_right] = (max_coordinate_value, max_coordinate_value)
        g.add_edge(top_left, top_left)
        g.add_edge(bottom_right, bottom_right)

        deg = g.degree_property_map("in")
        deg.a = 4 * (np.sqrt(deg.a) * 0.1 + 0.4)

        return GraphRenderingInfo(g, vertex_positions, deg, edge_weight, edge_length)
