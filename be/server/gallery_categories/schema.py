from marshmallow import fields, Schema

from be.server.utils import CamelCaseSchema


class GalleryCategorySchema(CamelCaseSchema):

    id = fields.Integer(default=None)
    title = fields.String()
    description = fields.String()
    freetext = fields.String()
    urlslug = fields.String()
