from marshmallow import fields

from be.server.utils import CamelCaseSchema
from be.server.vertex.schema import VertexSchema


class EdgeSchema(CamelCaseSchema):
    id = fields.Integer(default=None)
    graph_id = fields.Integer()
    src = fields.Nested(VertexSchema())
    trg = fields.Nested(VertexSchema())
    amount = fields.Float()


