from flask import Flask, jsonify  # ✅ include jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Technical Debt Tracker is running"

@app.route("/api")
def api():
    return jsonify({
        "status": "ok",
        "message": "API is working"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
