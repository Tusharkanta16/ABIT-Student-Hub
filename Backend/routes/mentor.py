from datetime import datetime

from flask import Blueprint, request, jsonify

from extensions import db
from models.mentor import MentorBooking


mentor_bp = Blueprint(
    "mentor",
    __name__,
    url_prefix="/api/mentor-bookings"
)


def booking_to_dict(booking):
    return {
        "id": booking.id,
        "mentor_name": booking.mentor_name,
        "mentor_email": booking.mentor_email,
        "student_name": booking.student_name,
        "student_email": booking.student_email,
        "session_topic": booking.session_topic,
        "session_date": booking.session_date.isoformat(),
        "duration_minutes": booking.duration_minutes,
        "status": booking.status,
        "created_at": booking.created_at.isoformat(),
        "updated_at": booking.updated_at.isoformat()
    }


# Create a mentor booking
@mentor_bp.route("/", methods=["POST"])
def create_booking():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    mentor_name = data.get("mentor_name")
    mentor_email = data.get("mentor_email")
    student_name = data.get("student_name")
    student_email = data.get("student_email")
    session_topic = data.get("session_topic")
    session_date = data.get("session_date")
    duration_minutes = data.get("duration_minutes")

    if (
        not mentor_name
        or not mentor_email
        or not student_name
        or not student_email
        or not session_topic
        or not session_date
        or duration_minutes is None
    ):
        return jsonify({
            "success": False,
            "message": "Mentor details, student details, session topic, session date and duration are required"
        }), 400

    try:
        parsed_session_date = datetime.fromisoformat(
            session_date.replace("Z", "+00:00")
        )
    except ValueError:
        return jsonify({
            "success": False,
            "message": "Invalid session date format. Use ISO format."
        }), 400

    try:
        duration_minutes = int(duration_minutes)
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Duration must be a valid number"
        }), 400

    if duration_minutes <= 0:
        return jsonify({
            "success": False,
            "message": "Duration must be greater than zero"
        }), 400

    booking = MentorBooking(
        mentor_name=mentor_name,
        mentor_email=mentor_email,
        student_name=student_name,
        student_email=student_email,
        session_topic=session_topic,
        session_date=parsed_session_date,
        duration_minutes=duration_minutes,
        status="Pending"
    )

    db.session.add(booking)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Mentor booking created successfully",
        "booking": booking_to_dict(booking)
    }), 201


# Get all mentor bookings
@mentor_bp.route("/", methods=["GET"])
def get_bookings():
    bookings = MentorBooking.query.order_by(
        MentorBooking.session_date.asc()
    ).all()

    return jsonify({
        "success": True,
        "bookings": [
            booking_to_dict(booking)
            for booking in bookings
        ]
    }), 200


# Get one mentor booking
@mentor_bp.route("/<int:booking_id>", methods=["GET"])
def get_booking(booking_id):
    booking = db.session.get(MentorBooking, booking_id)

    if not booking:
        return jsonify({
            "success": False,
            "message": "Mentor booking not found"
        }), 404

    return jsonify({
        "success": True,
        "booking": booking_to_dict(booking)
    }), 200


# Update a mentor booking
@mentor_bp.route("/<int:booking_id>", methods=["PUT"])
def update_booking(booking_id):
    booking = db.session.get(MentorBooking, booking_id)

    if not booking:
        return jsonify({
            "success": False,
            "message": "Mentor booking not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    if "mentor_name" in data:
        booking.mentor_name = data["mentor_name"]

    if "mentor_email" in data:
        booking.mentor_email = data["mentor_email"]

    if "student_name" in data:
        booking.student_name = data["student_name"]

    if "student_email" in data:
        booking.student_email = data["student_email"]

    if "session_topic" in data:
        booking.session_topic = data["session_topic"]

    if "session_date" in data:
        try:
            booking.session_date = datetime.fromisoformat(
                data["session_date"].replace("Z", "+00:00")
            )
        except ValueError:
            return jsonify({
                "success": False,
                "message": "Invalid session date format. Use ISO format."
            }), 400

    if "duration_minutes" in data:
        try:
            duration = int(data["duration_minutes"])

            if duration <= 0:
                return jsonify({
                    "success": False,
                    "message": "Duration must be greater than zero"
                }), 400

            booking.duration_minutes = duration

        except (TypeError, ValueError):
            return jsonify({
                "success": False,
                "message": "Duration must be a valid number"
            }), 400

    if "status" in data:
        booking.status = data["status"]

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Mentor booking updated successfully",
        "booking": booking_to_dict(booking)
    }), 200


# Delete a mentor booking
@mentor_bp.route("/<int:booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
    booking = db.session.get(MentorBooking, booking_id)

    if not booking:
        return jsonify({
            "success": False,
            "message": "Mentor booking not found"
        }), 404

    db.session.delete(booking)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Mentor booking deleted successfully"
    }), 200