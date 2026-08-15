from flask import Blueprint, request, jsonify

from extensions import db
from models.skill_exchange import SkillExchange


skill_exchange_bp = Blueprint(
    "skill_exchange",
    __name__,
    url_prefix="/api/skill-exchange"
)


def skill_to_dict(skill):
    return {
        "id": skill.id,
        "student_name": skill.student_name,
        "student_email": skill.student_email,
        "skill_offered": skill.skill_offered,
        "skill_wanted": skill.skill_wanted,
        "description": skill.description,
        "availability": skill.availability,
        "status": skill.status,
        "created_at": skill.created_at.isoformat(),
        "updated_at": skill.updated_at.isoformat()
    }


# Create a skill exchange listing
@skill_exchange_bp.route("/", methods=["POST"])
def create_skill_exchange():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    student_name = data.get("student_name")
    student_email = data.get("student_email")
    skill_offered = data.get("skill_offered")
    skill_wanted = data.get("skill_wanted")
    description = data.get("description")
    availability = data.get("availability")

    if (
        not student_name
        or not student_email
        or not skill_offered
        or not skill_wanted
        or not description
        or not availability
    ):
        return jsonify({
            "success": False,
            "message": "Student name, email, skill offered, skill wanted, description and availability are required"
        }), 400

    skill = SkillExchange(
        student_name=student_name,
        student_email=student_email,
        skill_offered=skill_offered,
        skill_wanted=skill_wanted,
        description=description,
        availability=availability,
        status="Available"
    )

    db.session.add(skill)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Skill exchange listing created successfully",
        "skill_exchange": skill_to_dict(skill)
    }), 201


# Get all skill exchange listings
@skill_exchange_bp.route("/", methods=["GET"])
def get_skill_exchanges():
    skills = SkillExchange.query.order_by(
        SkillExchange.created_at.desc()
    ).all()

    return jsonify({
        "success": True,
        "skill_exchanges": [
            skill_to_dict(skill)
            for skill in skills
        ]
    }), 200


# Get one skill exchange listing
@skill_exchange_bp.route("/<int:skill_id>", methods=["GET"])
def get_skill_exchange(skill_id):
    skill = db.session.get(SkillExchange, skill_id)

    if not skill:
        return jsonify({
            "success": False,
            "message": "Skill exchange listing not found"
        }), 404

    return jsonify({
        "success": True,
        "skill_exchange": skill_to_dict(skill)
    }), 200


# Update a skill exchange listing
@skill_exchange_bp.route("/<int:skill_id>", methods=["PUT"])
def update_skill_exchange(skill_id):
    skill = db.session.get(SkillExchange, skill_id)

    if not skill:
        return jsonify({
            "success": False,
            "message": "Skill exchange listing not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    if "student_name" in data:
        skill.student_name = data["student_name"]

    if "student_email" in data:
        skill.student_email = data["student_email"]

    if "skill_offered" in data:
        skill.skill_offered = data["skill_offered"]

    if "skill_wanted" in data:
        skill.skill_wanted = data["skill_wanted"]

    if "description" in data:
        skill.description = data["description"]

    if "availability" in data:
        skill.availability = data["availability"]

    if "status" in data:
        skill.status = data["status"]

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Skill exchange listing updated successfully",
        "skill_exchange": skill_to_dict(skill)
    }), 200


# Delete a skill exchange listing
@skill_exchange_bp.route("/<int:skill_id>", methods=["DELETE"])
def delete_skill_exchange(skill_id):
    skill = db.session.get(SkillExchange, skill_id)

    if not skill:
        return jsonify({
            "success": False,
            "message": "Skill exchange listing not found"
        }), 404

    db.session.delete(skill)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Skill exchange listing deleted successfully"
    }), 200