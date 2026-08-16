from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.user import User


users_bp = Blueprint(
    "users",
    __name__,
    url_prefix="/api/users"
)

@users_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):

    user = User.query.get(user_id)

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
            "department": user.department,
            "bio": user.bio,
            "skills": user.skills,
            "github_url": user.github_url,
            "linkedin_url": user.linkedin_url,
            "avatar_url": user.avatar_url
        }
    }), 200

@users_bp.route("/search", methods=["GET"])
@jwt_required()
def search_users():

    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({
            "success": False,
            "message": "Search query is required"
        }), 400

    users = User.query.filter(
        db.or_(
            User.name.ilike(f"%{query}%"),
            User.skills.ilike(f"%{query}%"),
            User.department.ilike(f"%{query}%")
        )
    ).limit(20).all()

    result = []

    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "department": user.department,
            "skills": user.skills,
            "avatar_url": user.avatar_url
        })

    return jsonify({
        "success": True,
        "users": result
    }), 200