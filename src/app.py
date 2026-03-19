from flask import Flask, jsonify, request, abort, Response
import os
import psutil
import logging
from dotenv import load_dotenv
from logging.handlers import TimedRotatingFileHandler
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import threading
import time
from flask_mail import Mail, Message

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Environment variables
APP_ENV = os.getenv("APP_ENV", "development")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
API_KEY = os.getenv("API_KEY", "default-api-key")

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")

mail = Mail(app)

# Logging setup
if not os.path.exists("logs"):
    os.makedirs("logs")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

if logger.hasHandlers():
    logger.handlers.clear()

file_handler = TimedRotatingFileHandler(
    "logs/application.log",
    when="midnight",
    interval=1,
    backupCount=30,
    encoding="utf-8"
)

console_handler = logging.StreamHandler()

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info("Application started")

# Prometheus metrics
cpu_usage = Gauge('cpu_usage_percent', 'CPU usage percent')
memory_usage = Gauge('memory_usage_percent', 'Memory usage percent')
disk_usage = Gauge('disk_usage_percent', 'Disk usage percent')

# Email alert function

def send_alert_email(subject, body):
    try:
        with app.app_context():

            recipient = os.getenv("MAIL_USERNAME")

            print("Sending email to:", recipient)

            msg = Message(
                subject=subject,
                recipients=[recipient]
            )
            msg.body = body

            mail.send(msg)

            print("EMAIL SENT SUCCESSFULLY")
            logger.info("Alert email sent")

    except Exception as e:
        print("EMAIL ERROR:", e)
        logger.error(f"Email failed: {e}")

# Background metrics + alert monitoring
def update_metrics():
    while True:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        cpu_usage.set(cpu)
        memory_usage.set(memory)
        disk_usage.set(disk)

        # Alert condition
        if cpu > 80:
            send_alert_email(
                "High CPU Alert",
                f"CPU usage is {cpu}%"
            )

        time.sleep(1)

# Start background thread
thread = threading.Thread(target=update_metrics)
thread.daemon = True
thread.start()

# Routes
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
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "environment": APP_ENV
    }), 200

@app.route("/test-email")
def test_email():
    send_alert_email("Test Alert", "Email is working!")
    return "Email sent!"

# Run app
if __name__ == "__main__":
    logger.info("Starting Flask server on port 8080")
    app.run(host="0.0.0.0", port=8080, debug=False)