from flask import Blueprint, request, jsonify

from extensions import db
from models.lost_found import LostFoundItem


lost_found_bp = Blueprint(
    "lost_found",
    __name__,
    url_prefix="/api/lost-found"
)


def item_to_dict(item):
    return {
        "id": item.id,
        "item_name": item.item_name,
        "description": item.description,
        "category": item.category,
        "location": item.location,
        "item_type": item.item_type,
        "reported_by": item.reported_by,
        "contact_email": item.contact_email,
        "status": item.status,
        "created_at": item.created_at.isoformat(),
        "updated_at": item.updated_at.isoformat()
    }


# Create a lost/found report
@lost_found_bp.route("/", methods=["POST"])
def create_item():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    item_name = data.get("item_name")
    description = data.get("description")
    category = data.get("category")
    location = data.get("location")
    item_type = data.get("item_type")
    reported_by = data.get("reported_by")
    contact_email = data.get("contact_email")

    if (
        not item_name
        or not description
        or not category
        or not location
        or not item_type
        or not reported_by
        or not contact_email
    ):
        return jsonify({
            "success": False,
            "message": "Item name, description, category, location, item type, reporter and contact email are required"
        }), 400

    if item_type not in ["Lost", "Found"]:
        return jsonify({
            "success": False,
            "message": "Item type must be either Lost or Found"
        }), 400

    item = LostFoundItem(
        item_name=item_name,
        description=description,
        category=category,
        location=location,
        item_type=item_type,
        reported_by=reported_by,
        contact_email=contact_email,
        status="Open"
    )

    db.session.add(item)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Lost and found report created successfully",
        "item": item_to_dict(item)
    }), 201


# Get all lost/found reports
@lost_found_bp.route("/", methods=["GET"])
def get_items():
    items = LostFoundItem.query.order_by(
        LostFoundItem.created_at.desc()
    ).all()

    return jsonify({
        "success": True,
        "items": [
            item_to_dict(item)
            for item in items
        ]
    }), 200


# Get one lost/found report
@lost_found_bp.route("/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = db.session.get(LostFoundItem, item_id)

    if not item:
        return jsonify({
            "success": False,
            "message": "Lost and found item not found"
        }), 404

    return jsonify({
        "success": True,
        "item": item_to_dict(item)
    }), 200


# Update a lost/found report
@lost_found_bp.route("/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = db.session.get(LostFoundItem, item_id)

    if not item:
        return jsonify({
            "success": False,
            "message": "Lost and found item not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    if "item_name" in data:
        item.item_name = data["item_name"]

    if "description" in data:
        item.description = data["description"]

    if "category" in data:
        item.category = data["category"]

    if "location" in data:
        item.location = data["location"]

    if "item_type" in data:
        if data["item_type"] not in ["Lost", "Found"]:
            return jsonify({
                "success": False,
                "message": "Item type must be either Lost or Found"
            }), 400

        item.item_type = data["item_type"]

    if "reported_by" in data:
        item.reported_by = data["reported_by"]

    if "contact_email" in data:
        item.contact_email = data["contact_email"]

    if "status" in data:
        item.status = data["status"]

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Lost and found report updated successfully",
        "item": item_to_dict(item)
    }), 200


# Delete a lost/found report
@lost_found_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = db.session.get(LostFoundItem, item_id)

    if not item:
        return jsonify({
            "success": False,
            "message": "Lost and found item not found"
        }), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Lost and found report deleted successfully"
    }), 200