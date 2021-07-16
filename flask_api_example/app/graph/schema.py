from marshmallow import fields, Schema


class GraphSchema(Schema):

    id = fields.Integer(data_key="id")
    owner = fields.String(data_key="owner")
    graph_name = fields.String(data_key="graphName")
    output_folder = fields.String(data_key="outputFolder")
    tile_size = fields.Integer(data_key="tileSize")
    zoom_levels = fields.Integer(data_key="zoomLevels")
    min_transparency = fields.Float(data_key="minTransparency")
    max_transparency = fields.Float(data_key="maxTransparency")
    tile_based_mean_transparency = fields.Float(data_key="tileBasedMeanTransparency")
    std_transparency_as_percentage = fields.Float(data_key="stdTransparencyAsPercentage")
    max_edge_thickness = fields.Float(data_key="maxEdgeThickness")
    med_edge_thickness = fields.Float(data_key="medEdgeThickness")
    max_vertex_size = fields.Float(data_key="maxVertexSize")
    med_vertex_size = fields.Float(data_key="medVertexSize")
    curvature = fields.Float(data_key="curvature")
    bg_color = fields.String(data_key="bgColor")
    source = fields.String(data_key="source")
    labels = fields.String(data_key="labels")
    median_pixel_distance = fields.Float(data_key="medianPixelDistance")
    min = fields.Float(data_key="min")
    max = fields.Float(data_key="max")
    vertices = fields.Integer(data_key="vertices")
    edges = fields.Integer(data_key="edges")