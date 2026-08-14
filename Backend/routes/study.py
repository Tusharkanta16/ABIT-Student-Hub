from flask import Blueprint, request, jsonify

from extensions import db
from models.study import StudyNote


study_bp = Blueprint(
    "study",
    __name__,
    url_prefix="/api/study"
)


# Create a study note
@study_bp.route("/", methods=["POST"])
def create_note():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    title = data.get("title")
    content = data.get("content")
    subject = data.get("subject")

    if not title or not content or not subject:
        return jsonify({
            "success": False,
            "message": "Title, content and subject are required"
        }), 400

    note = StudyNote(
        title=title,
        content=content,
        subject=subject
    )

    db.session.add(note)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Study note created successfully",
        "note": {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "subject": note.subject,
            "created_at": note.created_at.isoformat(),
            "updated_at": note.updated_at.isoformat()
        }
    }), 201


# Get all study notes
@study_bp.route("/", methods=["GET"])
def get_notes():
    notes = StudyNote.query.order_by(
        StudyNote.created_at.desc()
    ).all()

    note_list = []

    for note in notes:
        note_list.append({
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "subject": note.subject,
            "created_at": note.created_at.isoformat(),
            "updated_at": note.updated_at.isoformat()
        })

    return jsonify({
        "success": True,
        "notes": note_list
    }), 200


# Update a study note
@study_bp.route("/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    note = db.session.get(StudyNote, note_id)

    if not note:
        return jsonify({
            "success": False,
            "message": "Study note not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    if "title" in data:
        note.title = data["title"]

    if "content" in data:
        note.content = data["content"]

    if "subject" in data:
        note.subject = data["subject"]

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Study note updated successfully",
        "note": {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "subject": note.subject,
            "created_at": note.created_at.isoformat(),
            "updated_at": note.updated_at.isoformat()
        }
    }), 200


# Delete a study note
@study_bp.route("/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    note = db.session.get(StudyNote, note_id)

    if not note:
        return jsonify({
            "success": False,
            "message": "Study note not found"
        }), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Study note deleted successfully"
    }), 200