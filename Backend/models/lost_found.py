from datetime import datetime

from extensions import db


class LostFoundItem(db.Model):
    __tablename__ = "lost_found_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    item_name = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False
    )

    location = db.Column(
        db.String(200),
        nullable=False
    )

    item_type = db.Column(
        db.String(50),
        nullable=False
    )

    reported_by = db.Column(
        db.String(150),
        nullable=False
    )

    contact_email = db.Column(
        db.String(200),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Open",
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