from marshmallow import fields, Schema

from be.server.utils import CamelCaseSchema


class GraphSchema(CamelCaseSchema):

    id = fields.Integer()
    graph_name = fields.String()
    graph_category = fields.Integer()
    vertices = fields.Integer()
    edges = fields.Integer()
