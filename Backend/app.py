from flask import Flask, jsonify
from sqlalchemy import text

from config import Config
from extensions import db, migrate, jwt
from models.user import User
from models.notice import Notice
from models.study import Study
from models.placement import Placement
from models.complaint import Complaint

from routes.notices import notices_bp
from routes.study import study_bp
from routes.placements import placements_bp
from routes.complaints import complaints_bp
from routes.events import events_bp
from routes.marketplace import marketplace_bp
from routes.mentor import mentor_bp
from routes.lost_found import lost_found_bp
from routes.skill_exchange import skill_exchange_bp
from routes.auth import auth_bp
from routes.users import users_bp  # Import the users blueprint


app = Flask(__name__)

# Load configuration
app.config.from_object(Config)


# Initialize database and migration
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)

# Register feature routes
app.register_blueprint(notices_bp)
app.register_blueprint(study_bp)
app.register_blueprint(placements_bp)
app.register_blueprint(complaints_bp)
app.register_blueprint(events_bp)
app.register_blueprint(marketplace_bp)
app.register_blueprint(mentor_bp)
app.register_blueprint(lost_found_bp)
app.register_blueprint(skill_exchange_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)  # Register the users blueprint

@app.route("/")
def home():
    return "ABIT Student Hub Backend is Running!"


@app.route("/api/test")
def test_api():
    return jsonify({
        "success": True,
        "message": "ABIT Student Hub API is working!"
    })


@app.route("/api/db-test")
def db_test():
    try:
        db.session.execute(text("SELECT 1"))

        return jsonify({
            "success": True,
            "message": "MySQL connection is working!"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)