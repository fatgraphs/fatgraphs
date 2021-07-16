from marshmallow import fields, Schema


class VertexSchema(Schema):

    id = fields.Integer(attribute="id")
    # graph_id = Column(Integer(), ForeignKey('tg_graphs.id'))
    # metadata =  Column(Integer(), ForeignKey('tg_graphs.id'))
    eth = fields.String(attribute="eth")
    size = fields.Float(attribute="size")
    pos = fields.List(fields.Float(), attribute='pos')