from marshmallow import Schema, fields

from .author import AuthorSchema
from .revision import RevisionSchema


class ChangeRequestSchema(Schema):
    id = fields.UUID(dump_only=True)
    number = fields.Integer(dump_only=True)
    author = fields.Nested(AuthorSchema(), dump_only=True)
    parent_revision = fields.Nested(RevisionSchema())
    created_at = fields.DateTime(attribute="date_created", dump_only=True)
    provider = fields.Str(dump_only=True)
    external_id = fields.Str(dump_only=True)
    url = fields.Str(dump_only=True)
