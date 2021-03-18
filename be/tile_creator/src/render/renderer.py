import math
import os

from graph_tool.draw import graph_draw

from be.configuration import TILE_SOURCE
from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph
from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator


class GraphRenderer:

    def __init__(self, graph):
        if not isinstance(graph, GraphToolTokenGraph):
            raise TypeError("graph renderer needs an instance of GraphToolTokenGraph as argument")
        self.graph = graph

    def render_tiles(self, zoom_levels):
        tc = TransparencyCalculator(min(self.graph.edge_length.a), max(self.graph.edge_length.a),  zoom_levels)

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
                edge_colors[e] = (1, 1, 1, tc.get_transparency(edge_length, zoom_level))

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

    def _render(self, fit, file_name, edge_colors):
        graph_draw(self.graph.g,
                   pos=self.graph.vertex_positions,
                   bg_color='grey',
                   vertex_size=self.graph.degree,
                   vertex_fill_color=[1, 0, 0, 0.8],
                   edge_color=edge_colors,
                   output_size=[2048, 2048],
                   output=file_name,
                   fit_view=fit,
                   edge_pen_width=self.graph.edge_weight,
                   adjust_aspect=False,
                   fit_view_ink=True)
