from flask import Flask, jsonify
from sqlalchemy import text

from config import Config
from extensions import db, migrate
from routes.notices import notices_bp


app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Initialize database and migration
db.init_app(app)
migrate.init_app(app, db)

# Register Notice Board routes
app.register_blueprint(notices_bp)


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