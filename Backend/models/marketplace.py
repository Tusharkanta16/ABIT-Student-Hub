from datetime import datetime

from extensions import db


class MarketplaceItem(db.Model):
    __tablename__ = "marketplace_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    seller_name = db.Column(
        db.String(150),
        nullable=False
    )

    seller_email = db.Column(
        db.String(200),
        nullable=False
    )

    title = db.Column(
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

    price = db.Column(
        db.Float,
        nullable=False
    )

    condition = db.Column(
        db.String(50),
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