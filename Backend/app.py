from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "ABIT Student Hub Backend is Running!"


@app.route("/api/test")
def test_api():
    return jsonify({
        "success": True,
        "message": "ABIT Student Hub API is working!"
    })


if __name__ == "__main__":
    app.run(debug=True)