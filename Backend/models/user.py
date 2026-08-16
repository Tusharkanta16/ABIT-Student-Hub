from datetime import datetime

from extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    registration_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    department = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    bio = db.Column(
        db.Text,
        nullable=True
    )

    skills = db.Column(
        db.Text,
        nullable=True
    )

    github_url = db.Column(
        db.String(255),
        nullable=True
    )

    linkedin_url = db.Column(
        db.String(255),
        nullable=True
    )

    avatar_url = db.Column(
        db.String(500),
        nullable=True
    )

    theme = db.Column(
        db.String(100),
        nullable=True
    )

    role = db.Column(
        db.String(30),
        nullable=False,
        default="student"
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
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

    def __repr__(self):
        return f"<User {self.email}>"