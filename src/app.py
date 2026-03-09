from flask import Flask, jsonify, request, abort
import os
import psutil
import logging
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

APP_ENV = os.getenv("APP_ENV", "development")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
API_KEY = os.getenv("API_KEY", "default-api-key")


@app.route("/")
def home():
    logging.info("Home endpoint accessed")
    return f"Technical Debt Tracker running in {APP_ENV} environment"


@app.route("/api")
def api_status():
    logging.info("API status checked")
    return jsonify({
        "status": "ok",
        "message": "API is working",
        "database": {
            "host": DB_HOST,
            "port": DB_PORT
        }
    })


@app.route("/secure-api")
def secure_api():
    key = request.headers.get("x-api-key")

    if key != API_KEY:
        logging.warning("Unauthorized API access attempt")
        abort(401)

    return jsonify({
        "message": "Authorized access",
        "environment": APP_ENV
    })


@app.route("/metrics")
def metrics():
    logging.info("Metrics endpoint accessed")

    data = {
        "cpu_usage_percent": psutil.cpu_percent(),
        "memory_usage_percent": psutil.virtual_memory().percent,
        "disk_usage_percent": psutil.disk_usage('/').percent
    }

    return jsonify(data)

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "environment": APP_ENV
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080) 