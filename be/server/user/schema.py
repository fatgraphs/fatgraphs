from marshmallow import fields, Schema

from be.server.utils import CamelCaseSchema


class UserSchema(CamelCaseSchema):
    """Widget schema"""

    name = fields.String()
    recent_metadata_searches = fields.List(fields.List(fields.String))