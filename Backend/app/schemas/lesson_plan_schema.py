from marshmallow import Schema, fields, validate


class LessonPlanSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    objective = fields.String(required=True, validate=validate.Length(min=1))
    summary = fields.String(required=True, validate=validate.Length(min=1))
    planned_date = fields.Date(required=True)
    discipline = fields.String(required=True, validate=validate.Length(min=1, max=100))
    contents = fields.String(load_default=None)
    support_resources = fields.String(load_default=None)
    tags = fields.String(load_default=None)


class LessonPlanUpdateSchema(Schema):
    title = fields.String(validate=validate.Length(min=1, max=200))
    objective = fields.String(validate=validate.Length(min=1))
    summary = fields.String(validate=validate.Length(min=1))
    planned_date = fields.Date()
    discipline = fields.String(validate=validate.Length(min=1, max=100))
    contents = fields.String(load_default=None)
    support_resources = fields.String(load_default=None)
    tags = fields.String(load_default=None)


class AISuggestionsSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1))
    discipline = fields.String(required=True, validate=validate.Length(min=1))
    summary = fields.String(required=True, validate=validate.Length(min=1))
