from marshmallow import Schema, fields

class LessonPlanSchema(Schema):

    title = fields.String(required=True)

    objective = fields.String(required=True)

    summary = fields.String(required=True)

    discipline = fields.String(required=True)

    contents = fields.String()

    resources = fields.String()

    tags = fields.String()