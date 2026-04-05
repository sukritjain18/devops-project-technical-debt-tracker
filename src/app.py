from flask import Flask, jsonify, request, abort, Response
import os
import psutil
import logging
from dotenv import load_dotenv
from logging.handlers import TimedRotatingFileHandler
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import threading
import time
import requests

# ------------------ LOAD ENV ------------------
load_dotenv()

app = Flask(__name__)

# ------------------ ENV VARIABLES ------------------
APP_ENV = os.getenv("APP_ENV", "development")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
API_KEY = os.getenv("API_KEY", "default-api-key")

# ------------------ LOGGING ------------------
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

logger.info("🚀 Application started")

# ------------------ PROMETHEUS METRICS ------------------
cpu_usage = Gauge('cpu_usage_percent', 'CPU usage percent')
memory_usage = Gauge('memory_usage_percent', 'Memory usage percent')
disk_usage = Gauge('disk_usage_percent', 'Disk usage percent')

# ------------------ ALERT CONTROL ------------------
last_alert_time = 0
ALERT_COOLDOWN = 60  # seconds

def should_send_alert():
    global last_alert_time
    now = time.time()
    if now - last_alert_time > ALERT_COOLDOWN:
        last_alert_time = now
        return True
    return False

# ------------------ EMAIL FUNCTION ------------------

def send_alert_email(subject, body):
    api_key = os.getenv("SENDGRID_API_KEY")
    sender_email = os.getenv("MAIL_USERNAME")

    if not api_key:
        logger.warning("⚠️ SendGrid API key not configured")
        return

    if not sender_email:
        logger.warning("⚠️ Sender email not configured")
        return

    data = {
        "personalizations": [{
            "to": [{"email": sender_email}],
            "subject": subject
        }],
        "from": {"email": sender_email},
        "content": [{
            "type": "text/plain",
            "value": body
        }]
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            json=data,
            headers=headers,
            timeout=5
        )

        if response.status_code == 202:
            logger.info("✅ Email sent via SendGrid")
        else:
            logger.error(f"❌ SendGrid failed: {response.status_code} - {response.text}")

    except requests.exceptions.Timeout:
        logger.error("⏳ SendGrid request timed out")

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ SendGrid request error: {e}")

    except Exception as e:
        logger.error(f"❌ Unexpected email error: {e}")


def send_email_async(subject, body):
    try:
        thread = threading.Thread(
            target=send_alert_email,
            args=(subject, body),
            daemon=True
        )
        thread.start()
        logger.info("📨 Email task started in background")

    except Exception as e:
        logger.error(f"❌ Failed to start email thread: {e}")

# ------------------ METRICS MONITOR ------------------

def update_metrics():
    while True:
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent

            cpu_usage.set(cpu)
            memory_usage.set(memory)
            disk_usage.set(disk)

            logger.info(f"CPU: {cpu}%, Memory: {memory}%, Disk: {disk}%")

            # ALERT CONDITION
            if cpu > 80:
                if should_send_alert():
                    logger.info("⚠️ High CPU detected, sending alert...")
                    send_email_async(
                        "🚨 High CPU Alert",
                        f"CPU: {cpu}%\nMemory: {memory}%\nDisk: {disk}%"
                    )

            time.sleep(2)

        except Exception as e:
            logger.error(f"Metrics error: {e}")
            time.sleep(5)

# Start background thread
thread = threading.Thread(target=update_metrics, daemon=True)
thread.start()

# ------------------ ROUTES ------------------

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
    send_email_async("Test Alert", "Email is working!")
    return "Email sent!", 200
# ------------------ RUN ------------------

if __name__ == "__main__":
    logger.info("🚀 Starting Flask server")
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)