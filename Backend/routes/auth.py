from flask import Blueprint, request, jsonify

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from extensions import db
from models.user import User

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    name = data.get("name", "").strip()
    registration_number = data.get(
        "registration_number",
        ""
    ).strip()

    department = data.get(
        "department",
        ""
    ).strip()

    email = data.get(
        "email",
        ""
    ).strip().lower()

    phone = data.get(
        "phone",
        ""
    ).strip()

    password = data.get(
        "password",
        ""
    )

    # Required fields
    if not all([
        name,
        registration_number,
        department,
        email,
        phone,
        password
    ]):
        return jsonify({
            "success": False,
            "message": "All required fields must be provided"
        }), 400

    # ABIT email validation
    if not email.endswith("@abit.edu.in"):
        return jsonify({
            "success": False,
            "message": "Please use your ABIT college email"
        }), 400

    # Check existing email
    existing_email = User.query.filter_by(
        email=email
    ).first()

    if existing_email:
        return jsonify({
            "success": False,
            "message": "Email is already registered"
        }), 409

    # Check registration number
    existing_reg = User.query.filter_by(
        registration_number=registration_number
    ).first()

    if existing_reg:
        return jsonify({
            "success": False,
            "message": "Registration number is already registered"
        }), 409

    # Hash password
    password_hash = generate_password_hash(
        password
    )

    user = User(
        name=name,
        registration_number=registration_number,
        department=department,
        email=email,
        phone=phone,
        password_hash=password_hash,
        role="student"
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Account registered successfully"
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    email = data.get(
        "email",
        ""
    ).strip().lower()

    password = data.get(
        "password",
        ""
    )

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid email or password"
        }), 401

    if not user.is_active:
        return jsonify({
            "success": False,
            "message": "Your account is inactive"
        }), 403

    if not check_password_hash(
        user.password_hash,
        password
    ):
        return jsonify({
            "success": False,
            "message": "Invalid email or password"
        }), 401

    access_token = create_access_token(
        identity=str(user.id)
    )

    return jsonify({
        "success": True,
        "message": "Login successful",

        "access_token": access_token,

        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "registration_number": user.registration_number,
            "department": user.department,
            "phone": user.phone,
            "role": user.role
        }
    }), 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():

    user_id = get_jwt_identity()

    user = User.query.get(int(user_id))

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    return jsonify({
        "success": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "registration_number": user.registration_number,
            "department": user.department,
            "phone": user.phone,
            "bio": user.bio,
            "skills": user.skills,
            "github_url": user.github_url,
            "linkedin_url": user.linkedin_url,
            "avatar_url": user.avatar_url,
            "theme": user.theme,
            "role": user.role
        }
    }), 200

@auth_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():

    user_id = get_jwt_identity()

    user = User.query.get(int(user_id))

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    data = request.get_json()

    if "name" in data:
        user.name = data["name"].strip()

    if "phone" in data:
        user.phone = data["phone"].strip()

    if "bio" in data:
        user.bio = data["bio"].strip()

    if "skills" in data:
        user.skills = data["skills"].strip()

    if "github_url" in data:
        user.github_url = data["github_url"].strip()

    if "linkedin_url" in data:
        user.linkedin_url = data["linkedin_url"].strip()

    if "avatar_url" in data:
        user.avatar_url = data["avatar_url"].strip()

    if "theme" in data:
        user.theme = data["theme"].strip()

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Profile updated successfully"
    }), 200

@auth_bp.route("/change-password", methods=["PUT"])
@jwt_required()
def change_password():

    user_id = get_jwt_identity()

    user = User.query.get(int(user_id))

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    data = request.get_json()

    current_password = data.get(
        "current_password",
        ""
    )

    new_password = data.get(
        "new_password",
        ""
    )

    if not current_password or not new_password:
        return jsonify({
            "success": False,
            "message": "Current and new passwords are required"
        }), 400

    if not check_password_hash(
        user.password_hash,
        current_password
    ):
        return jsonify({
            "success": False,
            "message": "Current password is incorrect"
        }), 401

    if len(new_password) < 8:
        return jsonify({
            "success": False,
            "message": "New password must contain at least 8 characters"
        }), 400

    user.password_hash = generate_password_hash(
        new_password
    )

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Password changed successfully"
    }), 200