from marshmallow import fields

from be.server.utils import CamelCaseSchema
from be.server.vertex.schema import (
    VertexSchema,
    VertexSchemaPointConversion,
)

class EdgeSchemaConvertingPos(CamelCaseSchema):
    id = fields.Integer(default=None)
    graph_id = fields.Integer()
    src = fields.Nested(VertexSchemaPointConversion())
    trg = fields.Nested(VertexSchemaPointConversion())
    amount = fields.Float()

