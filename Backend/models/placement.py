from datetime import datetime

from extensions import db


class Placement(db.Model):
    __tablename__ = "placements"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    company = db.Column(
        db.String(200),
        nullable=False
    )

    job_title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    eligibility = db.Column(
        db.Text,
        nullable=False
    )

    location = db.Column(
        db.String(200),
        nullable=False
    )

    application_link = db.Column(
        db.String(500),
        nullable=True
    )

    deadline = db.Column(
        db.DateTime,
        nullable=True
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
    