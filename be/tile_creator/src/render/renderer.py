import math
import os
import numpy as np
from graph_tool.draw import graph_draw

from be.configuration import TILE_SOURCE, CONFIGURATIONS
from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator


class GraphRenderer:

    # TODO consider passing the configuration object to
    # the GraphRenderer constructor so it's more flexible
    # (rn is relying on the global config)
    def __init__(self, graph, tile_size=None):
        if not isinstance(graph, GraphToolTokenGraph):
            raise TypeError("graph renderer needs an instance of GraphToolTokenGraph as argument")
        self.graph = graph
        self.tile_size = tile_size

    def render_tiles(self, zoom_levels):
        tc = TransparencyCalculator(min(self.graph.edge_length.a), max(self.graph.edge_length.a))

        for zoom_level in range(0, zoom_levels):
            number_of_images = 4 ** zoom_level
            divide_by = int(math.sqrt(number_of_images))
            tuples = []
            for x in range(0, divide_by):
                for y in range(0, divide_by):
                    tuples.append((x, y))

            # edge colors are calculated at render time because transparency depends on zoom level
            edge_colors = self.graph.g.new_edge_property("vector<double>")
            for e in self.graph.g.edges():
                edge_length = self.graph.edge_length[e]
                transparency = tc.get_transparency(edge_length, zoom_level)
                edge_colors[e] = (1, 1, 1, transparency)

            for t in tuples:
                # TODO: check that width and height are the same: in thoery we implicityl rely on this equality
                fit = (
                    round(self.graph.min_x + ((self.graph.side / divide_by) * t[0]), 2),
                    round(self.graph.min_y + ((self.graph.side / divide_by) * t[1]), 2),
                    round(self.graph.side / divide_by, 2),
                    round(self.graph.side / divide_by, 2))

                print(fit)

                tile_name = "z_" + str(zoom_level) + "x_" + str(t[0]) + "y_" + str(t[1]) + ".png"
                file_name = os.path.join(TILE_SOURCE, tile_name)

                self._render(fit, file_name, edge_colors)
            # This ensures that vertices and edges maintain the same apparent size when zooming.
            # Without it you would notice that vertices and edges shrink when zooming.
            self.graph.degree.a = self.graph.degree.a * 2
            self.graph.edge_weight.a = self.graph.edge_weight.a * 2

    def _render(self, fit, file_name, edge_colors):
        if self.tile_size is not None:
            output_size = [self.tile_size, self.tile_size]
        else:
            output_size = [CONFIGURATIONS['tile_size'], CONFIGURATIONS['tile_size']]
        graph_draw(self.graph.g,
                   pos=self.graph.vertex_positions,
                   bg_color=CONFIGURATIONS['bg_color'],
                   vertex_size=self.graph.degree,
                   vertex_fill_color=[1, 0, 0, 0.8],
                   edge_color=edge_colors,
                   output_size=output_size,
                   output=file_name,
                   fit_view=fit,
                   edge_pen_width=self.graph.edge_weight,
                   adjust_aspect=False,
                   fit_view_ink=True)

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
