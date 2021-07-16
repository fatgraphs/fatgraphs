from marshmallow import fields, Schema


class MetadataSchema(Schema):
    id = fields.Integer(attribute="id")
    eth_target = fields.String(attribute="eth_target")
    eth_source = fields.String(attribute="eth_source")
    meta_type = fields.String(attribute="meta_type")
    meta_value = fields.String(attribute="meta_value")
    entity = fields.String(attribute="entity")


class AutocompleteTermSchema(Schema):
    meta_type = fields.String(attribute="meta_type")
    meta_value = fields.String(attribute="meta_value")
