from flask import Blueprint, request, jsonify

from extensions import db
from models.notice import Notice


notices_bp = Blueprint("notices", __name__, url_prefix="/api/notices")


@notices_bp.route("/", methods=["POST"])
def create_notice():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    title = data.get("title")
    content = data.get("content")
    category = data.get("category")
    posted_by = data.get("posted_by")

    if not title or not content or not category:
        return jsonify({
            "success": False,
            "message": "Title, content and category are required"
        }), 400

    notice = Notice(
        title=title,
        content=content,
        category=category,
        posted_by=posted_by
    )

    db.session.add(notice)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Notice created successfully",
        "notice": {
            "id": notice.id,
            "title": notice.title,
            "content": notice.content,
            "category": notice.category,
            "posted_by": notice.posted_by
        }
    }), 201


@notices_bp.route("/", methods=["GET"])
def get_notices():
    notices = Notice.query.order_by(Notice.created_at.desc()).all()

    notice_list = []

    for notice in notices:
        notice_list.append({
            "id": notice.id,
            "title": notice.title,
            "content": notice.content,
            "category": notice.category,
            "posted_by": notice.posted_by,
            "created_at": notice.created_at.isoformat(),
            "updated_at": notice.updated_at.isoformat()
        })

    return jsonify({
        "success": True,
        "notices": notice_list
    }), 200