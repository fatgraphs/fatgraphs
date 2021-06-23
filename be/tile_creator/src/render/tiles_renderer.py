import asyncio
import math
import os
from copy import deepcopy
from multiprocessing.context import Process

import numpy as np
from graph_tool.draw import graph_draw
import pandas as pd
from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator


class TilesRenderer:

    def __init__(self, gt_graph, visual_layout, metadata, transparency_calculator, configurations):
        if not isinstance(gt_graph, GraphToolTokenGraph):
            raise TypeError("graph renderer needs an instance of GraphToolTokenGraph as argument")
        self.gt_graph = gt_graph
        self.edge_transparencies = visual_layout.edge_transparencies
        self.vertex_shapes = visual_layout.vertex_shapes
        self.metadata = metadata
        self.configurations = configurations
        self.transparency_calculator = transparency_calculator
        self.tasks = []

    def render(self):
        rgba = [[1.0] * len(self.edge_transparencies[0])] * 4

        for zoom_level in range(0, self.configurations['zoom_levels']):
            vertex_size = deepcopy(self.gt_graph.vertex_sizes)
            edge_size = deepcopy(self.gt_graph.edge_thickness)

            rgba[3] = list(self.edge_transparencies[zoom_level].to_numpy())
            edge_colors = self.gt_graph.edge_transparencies[zoom_level]
            edge_colors.set_2d_array(np.array(rgba))

            number_of_images = 4 ** zoom_level
            divide_by = int(math.sqrt(number_of_images))
            tuples = []
            for x in range(0, divide_by):
                for y in range(0, divide_by):
                    tuples.append((x, y))


            for t in tuples:
                # TODO: check that width and height are the same: in thoery we implicityl rely on this equality

                min_coordinate = self.metadata.get_min_coordinate()
                max_coordinate = self.metadata.get_max_coordinate()
                side = max_coordinate - min_coordinate

                fit = (
                    round(min_coordinate + ((side / divide_by) * t[0]), 2),
                    round(min_coordinate + ((side / divide_by) * t[1]), 2),
                    round(side / divide_by, 2),
                    round(side / divide_by, 2))

                tile_name = "z_" + str(zoom_level) + "x_" + str(t[0]) + "y_" + str(t[1]) + ".png"
                file_name = os.path.join(self.configurations['output_folder'], tile_name)

                # Serial code
                # self._render(fit, file_name, edge_colors, vertex_size, edge_size)

                # Parallel code
                p = Process(target=self._render, args=(fit, file_name, edge_colors, vertex_size, edge_size))
                self.tasks.append(p)

            # This ensures that vertices and edges maintain the same apparent size when zooming.
            # Without it you would notice that vertices and edges shrink when zooming.
            self.gt_graph.vertex_sizes.a *= 2
            self.gt_graph.edge_thickness.a *= 2
        # Parallel code
        for p in self.tasks:
            p.start()
        for p in self.tasks:
            p.join()

    def _render(self, fit, file_name, edge_colors, vertex_size, edge_size):
        # if np.isnan(self.gt_graph.vertex_positions.get_2d_array([0, 1])).any() or \
        #         np.isnan(vertex_size.a).any() or \
        #         np.isnan(edge_size.a).any():
        #     raise Exception("Something is wrong")

        # print(self.gt_graph.vertex_positions.get_2d_array([0,1]))
        # print(edge_colors.get_2d_array([0,1,2,3]))

        graph_draw(self.gt_graph.g,
                   pos=self.gt_graph.vertex_positions,
                   bg_color=self.configurations['bg_color'],
                   vertex_size=vertex_size,
                   vertex_shape=self.gt_graph.vertex_shapes,
                   vertex_fill_color=[1, 0, 0, 0.8],
                   output_size=[self.configurations['tile_size'], self.configurations['tile_size']],
                   output=file_name,
                   edge_color=edge_colors,
                   fit_view=fit,
                   edge_pen_width=edge_size,
                   adjust_aspect=False,
                   fit_view_ink=True,
                   edge_control_points=self.gt_graph.control_points,
                   edge_end_marker="none")
        print(fit)


# DEBUG CODE - DONT DELETE

# run this code to instanciate the properties
'''
e_txt = self.graph.g.new_edge_property("string")
for e in self.graph.g.edges():
    e_txt[e] = str(round(self.graph.edge_length[e], 1))

v_txt = self.graph.g.new_vertex_property("string")
for v in self.graph.g.vertices():
    v_txt[v] = str(round(self.graph.vertex_positions[v][0], 1)) \
               + " " + str(round(self.graph.vertex_positions[v][1], 1))
'''

# add those argument to the graph_draw function to display useful debug info on the graph rendering
'''
edge_text=e_txt
edge_font_family="Times",
edge_text_color='red',
edge_font_size=18,
edge_text_parallel=True,
vertex_text=v_txt,
vertex_text_color='red',
vertex_font_size=12,
vertex_font_family="Times",
vertex_text_position='centered'
'''
