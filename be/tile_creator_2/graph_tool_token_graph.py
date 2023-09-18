import fnmatch
import os
from os import listdir
from os.path import join

import cairo
import cudf
import numpy as np
from graph_tool import Graph

from be.configuration import CONFIGURATIONS, PROJECT_ROOT


def ensure_list_like(func):
    def inner(self, list_like):
        try:
            list_like = list_like.values
        except Exception:
            if isinstance(list_like, cudf.Series):
                # .values not implemented in cudf for series of strings
                list_like = list_like.to_numpy()
        func(self, list_like)

    return inner


class GraphToolTokenGraph:
    '''
    This contains a token graph that is specifically used with the library graph_tool.
    An instacne of GraphToolTokenGraph contains all the static information needed to render a graph.
    '''

    def __init__(self):

        self.g = Graph(directed=True)
        self.vertex_positions = None
        self.edge_length = None
        self.vertex_sizes = None
        self.vertex_shapes = None
        self.edge_thicknesses = None
        self.control_points = None
        self.edge_transparencies = []

    @ensure_list_like
    def set_edges(self, edge_list):
        # hashed = False ensure that vertex values correspond to vertex indices
        self.g.add_edge_list(
            edge_list, hashed=False)

    @ensure_list_like
    def set_vertex_position(self, positions):
        self.vertex_positions = self.g.new_vertex_property("vector<float>",
                                                           vals=positions)

    @ensure_list_like
    def set_edge_length(self, edge_lengths):
        self.edge_length = self.g.new_edge_property("float", vals=edge_lengths)

    @ensure_list_like
    def set_vertex_size(self, vertex_sizes):
        self.vertex_sizes = self.g.new_vertex_property('float', vals=vertex_sizes)

    def set_bezier_points(self, global_curvature):
        """
        [x1, y1, x2, y2, x3, y3]
        the coordinates are relative: (x1,y1)=(0,0) refers to the source vertex
        (x3, y3)=(1,0) refers to the target vertex
        x2 and x3 are the percentage of the edge length at which a bezier
        point is placed, curvature specifies the common y of those 2 points
        :param curvature:
        :return:
        """
        self.control_points = self.g.new_edge_property('vector<float>')
        for v in self.g.vertices():
            for e in v.out_edges():
                curvature = round(self.edge_length[e] * global_curvature * -1, 2)
                self.control_points[e] = [0.0, 0.0, 0.25, curvature, 0.75, curvature, 1.0, 0.0]

    @ensure_list_like
    def set_shapes(self, string_shapes):
        """
        string_shapes is a sequence of strigns denoting what kind of shape (ie png image) should be used to render
        the  vertex.
        """

        def get_token_icon_mapper():
            custom_icons_file_name = fnmatch.filter(
                listdir(os.path.join(PROJECT_ROOT, CONFIGURATIONS['icons']['token_icons_home'])), "*.png")

            custom_icons_full_path = [
                os.path.abspath(join(PROJECT_ROOT, CONFIGURATIONS['icons']['token_icons_home'], f)) 
                for f 
                in custom_icons_file_name
            ]

            token_icon_paths = [cairo.ImageSurface.create_from_png(f) for f in custom_icons_full_path]

            token_icon_mapper = dict(zip(custom_icons_file_name, token_icon_paths))

            return token_icon_mapper

        def get_icons_mappper():
            eoa = cairo.ImageSurface.create_from_png(
                os.path.join(PROJECT_ROOT, CONFIGURATIONS['icons']["eoa"]))

            eoa_labelled = cairo.ImageSurface.create_from_png(
                os.path.join(PROJECT_ROOT, CONFIGURATIONS['icons']["eoa_labelled"]))

            ca = cairo.ImageSurface.create_from_png(
                os.path.join(PROJECT_ROOT, CONFIGURATIONS['icons']["ca"]))

            ca_labelled = cairo.ImageSurface.create_from_png(
                os.path.join(PROJECT_ROOT, CONFIGURATIONS['icons']["ca_labelled"]))

            inactive_fake = cairo.ImageSurface.create_from_png(
                os.path.join(PROJECT_ROOT, CONFIGURATIONS['icons']["inactive_fake"]))

            result = {
                'eoa_unlabelled': eoa,
                'eoa_labelled': eoa_labelled,
                'ca_unlabelled': ca,
                'ca_labelled': ca_labelled,
                'inactive_fake': inactive_fake
            }
            return result

        def string_to_cairosurface(map_object):
            # TODO: it can happen that a string_shape (defining the vertex image to use to render a vertex)
            # has no correspondance in the icons folder. In  this case it'd be better to have a fallback icon.

            def inner(key):
                if key in map_object:
                    return map_object[key]
                return map_object['ca_labelled']

            return inner


        generic_icons_mapper = get_icons_mappper()
        token_icon_mapper = get_token_icon_mapper()
        icon_mapper = {**generic_icons_mapper, **token_icon_mapper}
        vertex_cairo_surfaces = list(map(string_to_cairosurface(icon_mapper), string_shapes))
        self.vertex_shapes = self.g.new_vertex_property('object', vals=vertex_cairo_surfaces)

    @ensure_list_like
    def set_edge_thickness(self, thicnkesses):
        self.edge_thicknesses = self.g.new_edge_property("float", vals=thicnkesses)

    def set_edge_transparencies(self, edge_transparencies: dict):
        # edge transparency needs to be populated at run-time
        self.edge_transparencies = []
        # TODO: assuming that default edge color is always white, i.e. [1,1,1]
        rgba = [[1.0] * len(edge_transparencies[0])] * 4

        for zl in edge_transparencies.keys():
            self.edge_transparencies.append(self.g.new_edge_property("vector<float>"))
            # the alpha is the 4th element in the rgba
            rgba[3] = list(edge_transparencies[zl].to_numpy())
            self.edge_transparencies[zl].set_2d_array(np.array(rgba))

    def get_edge_transparencies(self):
        return self.edge_transparencies

    def get_edge_thicknesses(self):
        return self.edge_thicknesses

    def get_vertex_sizes(self):
        return self.vertex_sizes

    def double_sizes_for_consistency(self):
        self.vertex_sizes.a *= 2
        self.edge_thicknesses.a *= 2
