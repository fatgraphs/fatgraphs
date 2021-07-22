from marshmallow import fields, Schema

from be.server.utils import CamelCaseSchema


class VertexMetadataSchema(CamelCaseSchema):
    id = fields.Integer()
    eth = fields.String()
    type = fields.String()
    label = fields.String()
    description = fields.String()