from flask import Blueprint, request, jsonify

from extensions import db
from models.complaint import Complaint


complaints_bp = Blueprint(
    "complaints",
    __name__,
    url_prefix="/api/complaints"
)


# Create a complaint
@complaints_bp.route("/", methods=["POST"])
def create_complaint():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    student_name = data.get("student_name")
    student_email = data.get("student_email")
    subject = data.get("subject")
    description = data.get("description")
    category = data.get("category")

    if not student_name or not student_email or not subject or not description or not category:
        return jsonify({
            "success": False,
            "message": "Student name, email, subject, description and category are required"
        }), 400

    complaint = Complaint(
        student_name=student_name,
        student_email=student_email,
        subject=subject,
        description=description,
        category=category,
        status="Pending"
    )

    db.session.add(complaint)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Complaint submitted successfully",
        "complaint": {
            "id": complaint.id,
            "student_name": complaint.student_name,
            "student_email": complaint.student_email,
            "subject": complaint.subject,
            "description": complaint.description,
            "category": complaint.category,
            "status": complaint.status,
            "created_at": complaint.created_at.isoformat(),
            "updated_at": complaint.updated_at.isoformat()
        }
    }), 201


# Get all complaints
@complaints_bp.route("/", methods=["GET"])
def get_complaints():
    complaints = Complaint.query.order_by(
        Complaint.created_at.desc()
    ).all()

    complaint_list = []

    for complaint in complaints:
        complaint_list.append({
            "id": complaint.id,
            "student_name": complaint.student_name,
            "student_email": complaint.student_email,
            "subject": complaint.subject,
            "description": complaint.description,
            "category": complaint.category,
            "status": complaint.status,
            "created_at": complaint.created_at.isoformat(),
            "updated_at": complaint.updated_at.isoformat()
        })

    return jsonify({
        "success": True,
        "complaints": complaint_list
    }), 200


# Get one complaint
@complaints_bp.route("/<int:complaint_id>", methods=["GET"])
def get_complaint(complaint_id):
    complaint = db.session.get(Complaint, complaint_id)

    if not complaint:
        return jsonify({
            "success": False,
            "message": "Complaint not found"
        }), 404

    return jsonify({
        "success": True,
        "complaint": {
            "id": complaint.id,
            "student_name": complaint.student_name,
            "student_email": complaint.student_email,
            "subject": complaint.subject,
            "description": complaint.description,
            "category": complaint.category,
            "status": complaint.status,
            "created_at": complaint.created_at.isoformat(),
            "updated_at": complaint.updated_at.isoformat()
        }
    }), 200


# Update a complaint
@complaints_bp.route("/<int:complaint_id>", methods=["PUT"])
def update_complaint(complaint_id):
    complaint = db.session.get(Complaint, complaint_id)

    if not complaint:
        return jsonify({
            "success": False,
            "message": "Complaint not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    if "student_name" in data:
        complaint.student_name = data["student_name"]

    if "student_email" in data:
        complaint.student_email = data["student_email"]

    if "subject" in data:
        complaint.subject = data["subject"]

    if "description" in data:
        complaint.description = data["description"]

    if "category" in data:
        complaint.category = data["category"]

    if "status" in data:
        complaint.status = data["status"]

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Complaint updated successfully",
        "complaint": {
            "id": complaint.id,
            "student_name": complaint.student_name,
            "student_email": complaint.student_email,
            "subject": complaint.subject,
            "description": complaint.description,
            "category": complaint.category,
            "status": complaint.status,
            "created_at": complaint.created_at.isoformat(),
            "updated_at": complaint.updated_at.isoformat()
        }
    }), 200


# Delete a complaint
@complaints_bp.route("/<int:complaint_id>", methods=["DELETE"])
def delete_complaint(complaint_id):
    complaint = db.session.get(Complaint, complaint_id)

    if not complaint:
        return jsonify({
            "success": False,
            "message": "Complaint not found"
        }), 404

    db.session.delete(complaint)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Complaint deleted successfully"
    }), 200