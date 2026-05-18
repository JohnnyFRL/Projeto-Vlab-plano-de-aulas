from datetime import datetime, timezone
from app.extensions import db


class LessonPlan(db.Model):
    __tablename__ = "lesson_plans"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    objective = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    planned_date = db.Column(db.Date, nullable=False)
    discipline = db.Column(db.String(100), nullable=False)
    contents = db.Column(db.Text, nullable=True)
    support_resources = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(300), nullable=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "objective": self.objective,
            "summary": self.summary,
            "planned_date": self.planned_date.isoformat() if self.planned_date else None,
            "discipline": self.discipline,
            "contents": self.contents,
            "support_resources": self.support_resources,
            "tags": self.tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
