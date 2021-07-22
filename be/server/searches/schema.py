from marshmallow import fields, Schema

from be.server.utils import CamelCaseSchema


class SearchTermSchema(CamelCaseSchema):

    type = fields.String()
    value = fields.String()