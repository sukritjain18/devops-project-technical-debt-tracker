from flask import Flask, jsonify, request, abort
import os
import psutil
import logging
from dotenv import load_dotenv
from logging.handlers import TimedRotatingFileHandler

# Load environment variables
load_dotenv()

# Create logs folder if not exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure ROOT logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Remove duplicate handlers 
if logger.hasHandlers():
    logger.handlers.clear()

# File handler (rotates daily, keeps 30 days)
file_handler = TimedRotatingFileHandler(
    "logs/application.log",
    when="midnight",
    interval=1,
    backupCount=30,
    encoding="utf-8"
)
file_handler.setLevel(logging.INFO)

# Console handler 
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Log format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info("Application started")

# Initialize Flask app
app = Flask(__name__)

# Environment variables
APP_ENV = os.getenv("APP_ENV", "development")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
API_KEY = os.getenv("API_KEY", "default-api-key")

ALERT_TEST_MODE = True


@app.route("/")
def home():
    logger.info("Home endpoint accessed")
    return f"Technical Debt Tracker running in {APP_ENV} environment"


@app.route("/api")
def api_status():
    logger.info("API status checked")
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
        logger.warning("Unauthorized API access attempt")
        abort(401)

    logger.info("Secure API accessed successfully")

    return jsonify({
        "message": "Authorized access",
        "environment": APP_ENV
    })


@app.route("/metrics")
def metrics():
    logger.info("Metrics endpoint accessed")

    data = {
        "cpu_usage_percent": psutil.cpu_percent(),
        "memory_usage_percent": psutil.virtual_memory().percent,
        "disk_usage_percent": psutil.disk_usage('/').percent
    }

    return jsonify(data)


@app.route("/health")
def health():
    if ALERT_TEST_MODE:
        logger.error("Application unhealthy - alert test triggered")
        return jsonify({
            "status": "unhealthy",
            "reason": "Alert test mode enabled"
        }), 500

    logger.info("Health check endpoint accessed")

    return jsonify({
        "status": "healthy",
        "environment": APP_ENV
    }), 200,

if __name__ == "__main__":
    logger.info("Starting Flask server on port 8080")
    app.run(host="0.0.0.0", port=8080, debug=False)