from marshmallow import fields, Schema

from be.server.utils import CamelCaseSchema


class GraphConfigurationSchema(CamelCaseSchema):

    id = fields.Integer()
    tile_size = fields.Integer()
    zoom_levels = fields.Integer()
    min_transparency = fields.Float()
    max_transparency = fields.Float()
    tile_based_mean_transparency = fields.Float()
    std_transparency_as_percentage = fields.Float()
    max_edge_thickness = fields.Float()
    med_edge_thickness = fields.Float()
    max_vertex_size = fields.Float()
    med_vertex_size = fields.Float()
    curvature = fields.Float()
    bg_color = fields.String()
    source = fields.String()
    median_pixel_distance = fields.Float()
    min = fields.Float()
    max = fields.Float()
    graph = fields.Integer()
