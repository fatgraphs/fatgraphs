from marshmallow import fields, Schema


class UserSchema(Schema):
    """Widget schema"""

    name = fields.String(attribute="name")
    recent_metadata_searches = fields.List(fields.String(attribute="recentMetadataSearches"))
    # pluck selects only one element from the nested schema
    # It's important to use a string for the nested schema, re-importing the schema will cause problems
    graphs = fields.Pluck('GraphSchema', "graph_name", many=True)

