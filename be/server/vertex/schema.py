from marshmallow import fields, Schema, pre_load, pre_dump

from be.server.utils import CamelCaseSchema


class VertexSchema(CamelCaseSchema):
    graph_id = fields.Integer()
    vertex = fields.String()
    size = fields.Float()
    x = fields.Float()
    y = fields.Float()


class VertexSchemaPos(CamelCaseSchema):
    graph_id = fields.Integer()
    vertex = fields.String()
    size = fields.Float()
    pos = fields.List(fields.Float())
    labels = fields.List(fields.String(), default=[])
    types = fields.List(fields.String(), default=[])
