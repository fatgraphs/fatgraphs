import marshmallow
from geoalchemy2 import WKBElement
from marshmallow import fields
from shapely.wkb import loads

from be.server.utils import CamelCaseSchema


class WKBPointToListField(fields.Field):
        
    def _serialize(self, value, attr, data, **kwargs):
        if value is None:
            print("value is None in _serialize")
            return None

        if isinstance(value, WKBElement):
            geom = loads(bytes(value.data))
            if geom.geom_type == 'Point':
                return [geom.x, geom.y]
            else:
                raise marshmallow.ValidationError('Expected a Point geometry')
        else:
            raise marshmallow.ValidationError('Invalid data type for WKBPointField')


class VertexSchemaPointConversion(CamelCaseSchema):
    graph_id = fields.Integer()
    vertex = fields.String()
    size = fields.Float()
    pos = WKBPointToListField()
    labels = fields.List(fields.String(), default=[])
    types = fields.List(fields.String(), default=[])