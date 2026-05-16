from app import db

class LessonPlan(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)

    objective = db.Column(db.Text, nullable=False)

    summary = db.Column(db.Text, nullable=False)

    discipline = db.Column(db.String(100), nullable=False)

    contents = db.Column(db.Text)

    resources = db.Column(db.Text)

    tags = db.Column(db.String(200))