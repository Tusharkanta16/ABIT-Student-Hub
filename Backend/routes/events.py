from datetime import datetime

from flask import Blueprint, request, jsonify

from extensions import db
from models.event import Event


events_bp = Blueprint(
    "events",
    __name__,
    url_prefix="/api/events"
)


def event_to_dict(event):
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "event_type": event.event_type,
        "venue": event.venue,
        "event_date": event.event_date.isoformat(),
        "organizer": event.organizer,
        "registration_link": event.registration_link,
        "created_at": event.created_at.isoformat(),
        "updated_at": event.updated_at.isoformat()
    }


# Create an event
@events_bp.route("/", methods=["POST"])
def create_event():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    title = data.get("title")
    description = data.get("description")
    event_type = data.get("event_type")
    venue = data.get("venue")
    event_date = data.get("event_date")
    organizer = data.get("organizer")
    registration_link = data.get("registration_link")

    if not title or not description or not event_type or not venue or not event_date or not organizer:
        return jsonify({
            "success": False,
            "message": "Title, description, event type, venue, event date and organizer are required"
        }), 400

    try:
        parsed_event_date = datetime.fromisoformat(
            event_date.replace("Z", "+00:00")
        )
    except ValueError:
        return jsonify({
            "success": False,
            "message": "Invalid event date format. Use ISO format."
        }), 400

    event = Event(
        title=title,
        description=description,
        event_type=event_type,
        venue=venue,
        event_date=parsed_event_date,
        organizer=organizer,
        registration_link=registration_link
    )

    db.session.add(event)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Event created successfully",
        "event": event_to_dict(event)
    }), 201


# Get all events
@events_bp.route("/", methods=["GET"])
def get_events():
    events = Event.query.order_by(
        Event.event_date.asc()
    ).all()

    return jsonify({
        "success": True,
        "events": [
            event_to_dict(event)
            for event in events
        ]
    }), 200


# Get one event
@events_bp.route("/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = db.session.get(Event, event_id)

    if not event:
        return jsonify({
            "success": False,
            "message": "Event not found"
        }), 404

    return jsonify({
        "success": True,
        "event": event_to_dict(event)
    }), 200


# Update an event
@events_bp.route("/<int:event_id>", methods=["PUT"])
def update_event(event_id):
    event = db.session.get(Event, event_id)

    if not event:
        return jsonify({
            "success": False,
            "message": "Event not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    if "title" in data:
        event.title = data["title"]

    if "description" in data:
        event.description = data["description"]

    if "event_type" in data:
        event.event_type = data["event_type"]

    if "venue" in data:
        event.venue = data["venue"]

    if "event_date" in data:
        try:
            event.event_date = datetime.fromisoformat(
                data["event_date"].replace("Z", "+00:00")
            )
        except ValueError:
            return jsonify({
                "success": False,
                "message": "Invalid event date format. Use ISO format."
            }), 400

    if "organizer" in data:
        event.organizer = data["organizer"]

    if "registration_link" in data:
        event.registration_link = data["registration_link"]

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Event updated successfully",
        "event": event_to_dict(event)
    }), 200


# Delete an event
@events_bp.route("/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = db.session.get(Event, event_id)

    if not event:
        return jsonify({
            "success": False,
            "message": "Event not found"
        }), 404

    db.session.delete(event)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Event deleted successfully"
    }), 200