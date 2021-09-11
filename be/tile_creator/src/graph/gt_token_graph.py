import fnmatch
import os
import cairo
from graph_tool import Graph
import numpy as np
from os import listdir
from os.path import isfile, join
from be.configuration import internal_id, CONFIGURATIONS


class GraphToolTokenGraph:
    '''
    This contains a token graph that is specifically used with the library graph_tool.
    An instacne of GraphToolTokenGraph contains all the static information needed to render a graph.
    '''

    def __init__(self, edgeIdsToAmount, visualLayout, metadata, edgeCurvature):
        self.metadata = metadata
        self.edgeCurvature = edgeCurvature if edgeCurvature < 0 else -1 * edgeCurvature
        self.g = Graph(directed=True)
        self.addEdges(edgeIdsToAmount)
        self.vertexPositions = self.g.new_vertex_property("vector<float>",
                                                      vals=visualLayout.vertexPositions[["x", "y"]].values)
        self.edgeLength = self.g.new_edge_property("float", vals=visualLayout.edgeLengths)
        self.vertexSizes = self.g.new_vertex_property('float', vals=visualLayout.vertexSizes)
        self.vertexShapes = self.make_shapes(visualLayout.vertexShapes)
        self.edgeThickness = self.g.new_edge_property("float", vals=visualLayout.edgeThickness)
        self.makeBezierPoints()
        # edge transparency needs to be populated at run-time
        self.edgeTransparencies = []
        rgba = [[1.0] * len(visualLayout.edgeTransparencies[0])] * 4

        for zl in range(0, metadata.getZoomLevels()):
            self.edgeTransparencies.append(self.g.new_edge_property("vector<float>"))
            rgba[3] = list(visualLayout.edgeTransparencies[zl].to_numpy()) # set alpha based on zoom
            self.edgeTransparencies[zl].set_2d_array(np.array(rgba))

    def makeBezierPoints(self):
        self.controlPoints = self.g.new_edge_property('vector<float>')
        for v in self.g.vertices():
            for e in v.out_edges():
                curvature = self.edgeLength[e] * self.edgeCurvature
                self.controlPoints[e] = [0, 0, 0.25, curvature, 0.75, curvature, 1, 0]

    def addEdges(self, edgeIdsToAmount):
        # data = edgeIdsToAmount.rename(columns={'sourceId': 'source', 'targetId': 'target'})
        # hashed = False ensure that vertex values correspond to vertex indices
        self.g.add_edge_list(
            edgeIdsToAmount[[internal_id('target'), internal_id('source')]].values,
            hashed=False)

    def make_shapes(self, string_shapes):

        def get_token_icon_mapper():
            custom_icons_file_name = fnmatch.filter(listdir(os.path.abspath(CONFIGURATIONS['icons']['token_icons_home'])), "*.png")

            custom_icons_full_path = [os.path.abspath(join(CONFIGURATIONS['icons']['token_icons_home'], f)) for f in custom_icons_file_name]

            token_icon_paths = [cairo.ImageSurface.create_from_png(f) for f in custom_icons_full_path]

            token_icon_mapper = dict(zip(custom_icons_file_name, token_icon_paths))

            return token_icon_mapper

        def get_icons_mappper():
            print(os.path.abspath(CONFIGURATIONS['icons']["eoa"]))
            eoa = cairo.ImageSurface.create_from_png(
                    os.path.abspath(CONFIGURATIONS['icons']["eoa"]))
            eoa_labelled = cairo.ImageSurface.create_from_png(
                    os.path.abspath(CONFIGURATIONS['icons']["eoa_labelled"]))
            ca = cairo.ImageSurface.create_from_png(
                os.path.abspath(CONFIGURATIONS['icons']["ca"]))
            ca_labelled = cairo.ImageSurface.create_from_png(
                    os.path.abspath(CONFIGURATIONS['icons']["ca_labelled"]))
            inactive_fake = cairo.ImageSurface.create_from_png(
                    os.path.abspath(CONFIGURATIONS['icons']["inactive_fake"]))
            result = {
                    'eoa_unlabelled': eoa,
                    'eoa_labelled': eoa_labelled,
                    'ca_unlabelled': ca,
                    'ca_labelled': ca_labelled,
                    'inactive_fake': inactive_fake
                }
            return result

        generic_icons_mapper = get_icons_mappper()
        token_icon_mapper = get_token_icon_mapper()
        icon_mapper = {**generic_icons_mapper, **token_icon_mapper}
        vertex_cairo_surfaces = list(map(lambda e: icon_mapper[e], string_shapes))
        return self.g.new_vertex_property('object', vals=vertex_cairo_surfaces)
