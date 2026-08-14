from datetime import datetime

from flask import Blueprint, request, jsonify

from extensions import db
from models.placement import Placement


placements_bp = Blueprint(
    "placements",
    __name__,
    url_prefix="/api/placements"
)


# Create a placement
@placements_bp.route("/", methods=["POST"])
def create_placement():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    company = data.get("company")
    job_title = data.get("job_title")
    description = data.get("description")
    eligibility = data.get("eligibility")
    location = data.get("location")
    application_link = data.get("application_link")
    deadline = data.get("deadline")

    if not company or not job_title or not description or not eligibility or not location:
        return jsonify({
            "success": False,
            "message": "Company, job title, description, eligibility and location are required"
        }), 400

    parsed_deadline = None

    if deadline:
        try:
            parsed_deadline = datetime.fromisoformat(
                deadline.replace("Z", "+00:00")
            )
        except ValueError:
            return jsonify({
                "success": False,
                "message": "Invalid deadline format. Use ISO format."
            }), 400

    placement = Placement(
        company=company,
        job_title=job_title,
        description=description,
        eligibility=eligibility,
        location=location,
        application_link=application_link,
        deadline=parsed_deadline
    )

    db.session.add(placement)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Placement created successfully",
        "placement": {
            "id": placement.id,
            "company": placement.company,
            "job_title": placement.job_title,
            "description": placement.description,
            "eligibility": placement.eligibility,
            "location": placement.location,
            "application_link": placement.application_link,
            "deadline": (
                placement.deadline.isoformat()
                if placement.deadline else None
            ),
            "created_at": placement.created_at.isoformat(),
            "updated_at": placement.updated_at.isoformat()
        }
    }), 201


# Get all placements
@placements_bp.route("/", methods=["GET"])
def get_placements():
    placements = Placement.query.order_by(
        Placement.created_at.desc()
    ).all()

    placement_list = []

    for placement in placements:
        placement_list.append({
            "id": placement.id,
            "company": placement.company,
            "job_title": placement.job_title,
            "description": placement.description,
            "eligibility": placement.eligibility,
            "location": placement.location,
            "application_link": placement.application_link,
            "deadline": (
                placement.deadline.isoformat()
                if placement.deadline else None
            ),
            "created_at": placement.created_at.isoformat(),
            "updated_at": placement.updated_at.isoformat()
        })

    return jsonify({
        "success": True,
        "placements": placement_list
    }), 200


# Get one placement
@placements_bp.route("/<int:placement_id>", methods=["GET"])
def get_placement(placement_id):
    placement = db.session.get(Placement, placement_id)

    if not placement:
        return jsonify({
            "success": False,
            "message": "Placement not found"
        }), 404

    return jsonify({
        "success": True,
        "placement": {
            "id": placement.id,
            "company": placement.company,
            "job_title": placement.job_title,
            "description": placement.description,
            "eligibility": placement.eligibility,
            "location": placement.location,
            "application_link": placement.application_link,
            "deadline": (
                placement.deadline.isoformat()
                if placement.deadline else None
            ),
            "created_at": placement.created_at.isoformat(),
            "updated_at": placement.updated_at.isoformat()
        }
    }), 200


# Update a placement
@placements_bp.route("/<int:placement_id>", methods=["PUT"])
def update_placement(placement_id):
    placement = db.session.get(Placement, placement_id)

    if not placement:
        return jsonify({
            "success": False,
            "message": "Placement not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    if "company" in data:
        placement.company = data["company"]

    if "job_title" in data:
        placement.job_title = data["job_title"]

    if "description" in data:
        placement.description = data["description"]

    if "eligibility" in data:
        placement.eligibility = data["eligibility"]

    if "location" in data:
        placement.location = data["location"]

    if "application_link" in data:
        placement.application_link = data["application_link"]

    if "deadline" in data:
        if data["deadline"]:
            try:
                placement.deadline = datetime.fromisoformat(
                    data["deadline"].replace("Z", "+00:00")
                )
            except ValueError:
                return jsonify({
                    "success": False,
                    "message": "Invalid deadline format. Use ISO format."
                }), 400
        else:
            placement.deadline = None

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Placement updated successfully",
        "placement": {
            "id": placement.id,
            "company": placement.company,
            "job_title": placement.job_title,
            "description": placement.description,
            "eligibility": placement.eligibility,
            "location": placement.location,
            "application_link": placement.application_link,
            "deadline": (
                placement.deadline.isoformat()
                if placement.deadline else None
            ),
            "created_at": placement.created_at.isoformat(),
            "updated_at": placement.updated_at.isoformat()
        }
    }), 200


# Delete a placement
@placements_bp.route("/<int:placement_id>", methods=["DELETE"])
def delete_placement(placement_id):
    placement = db.session.get(Placement, placement_id)

    if not placement:
        return jsonify({
            "success": False,
            "message": "Placement not found"
        }), 404

    db.session.delete(placement)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Placement deleted successfully"
    }), 200