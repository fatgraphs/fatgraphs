import math
import os
from copy import deepcopy
from multiprocessing.context import Process

import numpy as np
from graph_tool.draw import graph_draw

from be.configuration import MAX_CORES
from be.tile_creator.src.graph.gt_token_graph import GraphToolTokenGraph


class TilesRenderer:

    def __init__(self, gtGraph, metadata, configurations):
        if not isinstance(gtGraph, GraphToolTokenGraph):
            raise TypeError("graph renderer needs an instance of GraphToolTokenGraph as argument")
        self.gtGraph = gtGraph
        self.metadata = metadata
        self.configurations = configurations
        self.renderingProcesses = []

    def renderGraph(self):
        # rgba = [[1.0] * len(self.edgeTransparencies[0])] * 4

        for zoomLevel in range(0, self.configurations['zoom_levels']):
            vertexSize = deepcopy(self.gtGraph.vertexSizes)
            edgeSize = deepcopy(self.gtGraph.edgeThickness)

            # rgba[3] = list(self.edgeTransparencies[zoomLevel].to_numpy())
            # edgeColors = self.gtGraph.edgeTransparencies[zoomLevel]
            # edgeColors.set_2d_array(np.array(rgba))

            numberOfImages = 4 ** zoomLevel
            divideBy = int(math.sqrt(numberOfImages))
            tuples = []
            for x in range(0, divideBy):
                for y in range(0, divideBy):
                    tuples.append((x, y))

            for t in tuples:
                # TODO: check that width and height are the same: in thoery we implicityl rely on this equality

                minCoordinate = self.metadata.getMinCoordinate()
                maxCoordinate = self.metadata.getMaxCoordinate()
                side = maxCoordinate - minCoordinate

                fit = (
                    round(minCoordinate + ((side / divideBy) * t[0]), 2),
                    round(minCoordinate + ((side / divideBy) * t[1]), 2),
                    round(side / divideBy, 2),
                    round(side / divideBy, 2))

                tileName = "z_" + str(zoomLevel) + "x_" + str(t[0]) + "y_" + str(t[1]) + ".png"
                fileName = os.path.join(self.configurations['output_folder'], tileName)

                # Serial code
                # self._render(fit, file_name, edge_colors, vertex_size, edge_size)

                # Parallel code
                rendering_process = Process(target=self.render,
                                            args=(fit, fileName, self.gtGraph.edgeTransparencies[zoomLevel], vertexSize, edgeSize))
                self.renderingProcesses.append(rendering_process)

            # This ensures that vertices and edges maintain the same apparent size when zooming.
            # Without it you would notice that vertices and edges shrink when zooming.
            self.gtGraph.vertexSizes.a *= 2
            self.gtGraph.edgeThickness.a *= 2

        # Parallel code
        started = []
        for renderingProcess in self.renderingProcesses:

            if len(started) >= MAX_CORES:
                started[0].join()
                started = started[1::]
            renderingProcess.start()
            started.append(renderingProcess)

        for renderingProcess in started:
            renderingProcess.join()

    def render(self, fit, fileName, edgeColors, vertexSize, edgeSize):
        # if np.isnan(self.gt_graph.vertex_positions.get_2d_array([0, 1])).any() or \
        #         np.isnan(vertex_size.a).any() or \
        #         np.isnan(edge_size.a).any():
        #     raise Exception("Something is wrong")

        # print(self.gt_graph.vertex_positions.get_2d_array([0,1]))
        # print(edge_colors.get_2d_array([0,1,2,3]))

        graph_draw(self.gtGraph.g,
                   pos=self.gtGraph.vertexPositions,
                   # bg_color=self.configurations['bg_color'],
                   vertex_size=vertexSize,
                   vertex_anchor=0,
                   vertex_surface=self.gtGraph.vertexShapes,
                   vertex_color=[0.0, 0.0, 0.0, 0.0],
                   vertex_fill_color=[0.0, 0.0, 0.0, 0.0],
                   edge_sloppy=True,
                   output_size=[self.configurations['tile_size'], self.configurations['tile_size']],
                   output=fileName,
                   edge_color=edgeColors,
                   fit_view=fit,
                   edge_pen_width=edgeSize,
                   adjust_aspect=False,
                   fit_view_ink=True,
                   edge_control_points=self.gtGraph.controlPoints,
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
