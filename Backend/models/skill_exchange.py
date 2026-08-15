from datetime import datetime

from extensions import db


class SkillExchange(db.Model):
    __tablename__ = "skill_exchanges"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_name = db.Column(
        db.String(150),
        nullable=False
    )

    student_email = db.Column(
        db.String(200),
        nullable=False
    )

    skill_offered = db.Column(
        db.String(150),
        nullable=False
    )

    skill_wanted = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    availability = db.Column(
        db.String(200),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Available",
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )