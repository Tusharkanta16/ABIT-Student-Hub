from datetime import datetime

from extensions import db


class MentorBooking(db.Model):
    __tablename__ = "mentor_bookings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    mentor_name = db.Column(
        db.String(150),
        nullable=False
    )

    mentor_email = db.Column(
        db.String(200),
        nullable=False
    )

    student_name = db.Column(
        db.String(150),
        nullable=False
    )

    student_email = db.Column(
        db.String(200),
        nullable=False
    )

    session_topic = db.Column(
        db.String(250),
        nullable=False
    )

    session_date = db.Column(
        db.DateTime,
        nullable=False
    )

    duration_minutes = db.Column(
        db.Integer,
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Pending",
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