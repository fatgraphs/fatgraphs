from marshmallow import fields

from be.server.utils import CamelCaseSchema


class SearchTermSchema(CamelCaseSchema):

    type = fields.String()
    value = fields.String()