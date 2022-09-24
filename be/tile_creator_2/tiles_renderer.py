import functools
import math
import os
import time
from copy import deepcopy
from multiprocessing.context import Process

from graph_tool.draw import graph_draw

from be.configuration import MAX_CORES
from be.tile_creator_2.graph_tool_token_graph import GraphToolTokenGraph
from be.tile_creator_2.util.bound import Bound
from be.utils import timeit


class TilesRenderer:

    def __init__(self, gt_graph: GraphToolTokenGraph, output_folder, graph_space_bound: Bound, pixel_space_bound: Bound):
        self.gt_graph = gt_graph
        self.renderingProcesses = []
        self.output_folder = output_folder
        self.graph_space_bound = graph_space_bound
        self.pixel_space_bound = pixel_space_bound
        # to keep track of progress:
        self.tiles_to_render = 0
        self.render_count = 0

    @timeit("Rendering the tiles")
    def render_graph(self):
        self.tiles_to_render = functools.reduce(lambda a, b: a + b, map(lambda zoom_level : 4 ** zoom_level, range(0, self.zoom_levels())))

        for zoom_level in range(0, self.zoom_levels()):
            vertex_sizes = deepcopy(self.gt_graph.get_vertex_sizes())
            edge_sizes = deepcopy(self.gt_graph.get_edge_thicknesses())

            tile_count_this_zoom = 4 ** zoom_level # 1 tile --> 4 tiles --> 16 tiles ...
            divide_by = int(math.sqrt(tile_count_this_zoom))
            tuples = []
            for x in range(0, divide_by):
                for y in range(0, divide_by):
                    tuples.append((x, y))

            for t in tuples:
                x = round(self.graph_space_bound.get_min_coord() + ((self.graph_space_bound.get_side() / divide_by) * t[0]), 2)
                y = round(self.graph_space_bound.get_min_coord() + ((self.graph_space_bound.get_side() / divide_by) * t[1]), 2)
                w = round(self.graph_space_bound.get_side() / divide_by, 2)
                h = round(self.graph_space_bound.get_side() / divide_by, 2)
                fit_view = (x, y, w, h)

                tile_name = "z_" + str(zoom_level) + "x_" + str(t[0]) + "y_" + str(t[1]) + ".png"
                file_name = os.path.join(self.output_folder, tile_name)

                # Serial code
                # self.render(fit_view, file_name, self.gt_graph.get_edge_transparencies()[zoom_level], vertex_sizes, edge_sizes)

                # Parallel code
                rendering_process = Process(target=self.render,
                                            args=(fit_view, file_name,
                                                  self.gt_graph.get_edge_transparencies()[zoom_level],
                                                  vertex_sizes,
                                                  edge_sizes))
                self.renderingProcesses.append(rendering_process)

            # This ensures that vertices and edges maintain the same apparent size when zooming.
            # Without it you would notice that vertices and edges shrink when zooming.
            self.gt_graph.double_sizes_for_consistency()

        # Parallel code
        started = []
        for renderingProcess in self.renderingProcesses:
            renderingProcess.start()
            started.append(renderingProcess)
            if(len(started) >= MAX_CORES):
                started[0].join() # wait for process to complete
                started[0].close() # terminate process properly
                started = started[1::] # remove from active list
                self.print_progress()

        for renderingProcess in started:
            renderingProcess.join() # wait for process to complete
            renderingProcess.close() # terminate process properly
            self.print_progress()
            time.sleep(0.1)

    def zoom_levels(self):
        return len(self.gt_graph.get_edge_transparencies())

    def render(self, fit, file_name, edge_colors, vertex_size, edge_size):

        graph_draw(self.gt_graph.g,
                   pos=self.gt_graph.vertex_positions,
                   # bg_color=,
                   vertex_size=vertex_size,
                   vertex_anchor=0,
                   vertex_surface=self.gt_graph.vertex_shapes,
                   vertex_color=[0.0, 0.0, 0.0, 0.0],
                   vertex_fill_color=[0.0, 0.0, 0.0, 0.0],
                   edge_sloppy=True,
                   output_size=[self.pixel_space_bound.get_side(), self.pixel_space_bound.get_side()],
                   output=file_name,
                   edge_color=edge_colors,
                   fit_view=fit,
                   edge_pen_width=edge_size,
                   adjust_aspect=False,
                   fit_view_ink=True,
                   edge_control_points=self.gt_graph.control_points,
                   edge_end_marker="none")


    def print_progress(self):
        self.render_count += 1
        message = f"finished {self.render_count} of {self.tiles_to_render} tiles"
        if self.render_count == self.tiles_to_render:
            pass
        else:
            print(message, end="\r", flush=True)


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
