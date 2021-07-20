from marshmallow import fields, Schema

from be.server.utils import CamelCaseSchema


class MetadataSchema(CamelCaseSchema):
    id = fields.Integer()
    eth_target = fields.String()
    eth_source = fields.String(default='')
    meta_type = fields.String()
    meta_value = fields.String()
    entity = fields.String()


class AutocompleteTermSchema(CamelCaseSchema):
    meta_type = fields.String()
    meta_value = fields.String()
