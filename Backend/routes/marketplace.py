from flask import Blueprint, request, jsonify

from extensions import db
from models.marketplace import MarketplaceItem


marketplace_bp = Blueprint(
    "marketplace",
    __name__,
    url_prefix="/api/marketplace"
)


def item_to_dict(item):
    return {
        "id": item.id,
        "seller_name": item.seller_name,
        "seller_email": item.seller_email,
        "title": item.title,
        "description": item.description,
        "category": item.category,
        "price": item.price,
        "condition": item.condition,
        "status": item.status,
        "created_at": item.created_at.isoformat(),
        "updated_at": item.updated_at.isoformat()
    }


# Create a marketplace listing
@marketplace_bp.route("/", methods=["POST"])
def create_item():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    seller_name = data.get("seller_name")
    seller_email = data.get("seller_email")
    title = data.get("title")
    description = data.get("description")
    category = data.get("category")
    price = data.get("price")
    condition = data.get("condition")

    if (
        not seller_name
        or not seller_email
        or not title
        or not description
        or not category
        or price is None
        or not condition
    ):
        return jsonify({
            "success": False,
            "message": "Seller name, email, title, description, category, price and condition are required"
        }), 400

    try:
        price = float(price)
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Price must be a valid number"
        }), 400

    if price < 0:
        return jsonify({
            "success": False,
            "message": "Price cannot be negative"
        }), 400

    item = MarketplaceItem(
        seller_name=seller_name,
        seller_email=seller_email,
        title=title,
        description=description,
        category=category,
        price=price,
        condition=condition,
        status="Available"
    )

    db.session.add(item)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Marketplace item created successfully",
        "item": item_to_dict(item)
    }), 201


# Get all marketplace listings
@marketplace_bp.route("/", methods=["GET"])
def get_items():
    items = MarketplaceItem.query.order_by(
        MarketplaceItem.created_at.desc()
    ).all()

    return jsonify({
        "success": True,
        "items": [
            item_to_dict(item)
            for item in items
        ]
    }), 200


# Get one marketplace listing
@marketplace_bp.route("/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = db.session.get(MarketplaceItem, item_id)

    if not item:
        return jsonify({
            "success": False,
            "message": "Marketplace item not found"
        }), 404

    return jsonify({
        "success": True,
        "item": item_to_dict(item)
    }), 200


# Update a marketplace listing
@marketplace_bp.route("/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = db.session.get(MarketplaceItem, item_id)

    if not item:
        return jsonify({
            "success": False,
            "message": "Marketplace item not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    if "seller_name" in data:
        item.seller_name = data["seller_name"]

    if "seller_email" in data:
        item.seller_email = data["seller_email"]

    if "title" in data:
        item.title = data["title"]

    if "description" in data:
        item.description = data["description"]

    if "category" in data:
        item.category = data["category"]

    if "price" in data:
        try:
            new_price = float(data["price"])

            if new_price < 0:
                return jsonify({
                    "success": False,
                    "message": "Price cannot be negative"
                }), 400

            item.price = new_price

        except (TypeError, ValueError):
            return jsonify({
                "success": False,
                "message": "Price must be a valid number"
            }), 400

    if "condition" in data:
        item.condition = data["condition"]

    if "status" in data:
        item.status = data["status"]

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Marketplace item updated successfully",
        "item": item_to_dict(item)
    }), 200


# Delete a marketplace listing
@marketplace_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = db.session.get(MarketplaceItem, item_id)

    if not item:
        return jsonify({
            "success": False,
            "message": "Marketplace item not found"
        }), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Marketplace item deleted successfully"
    }), 200