from marshmallow import fields

from be.server.utils import CamelCaseSchema


class VertexSchema(CamelCaseSchema):
    graph_id = fields.Integer()
    vertex = fields.String()
    size = fields.Float()
    pos = fields.List(fields.Float())
    labels = fields.List(fields.String(), default=[])
    types = fields.List(fields.String(), default=[])
