from flask import Flask, jsonify
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env if running locally

app = Flask(__name__)

APP_ENV = os.getenv("APP_ENV")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
API_KEY = os.getenv("API_KEY")

@app.route("/")
def home():
    return f"Technical Debt Tracker is running in {APP_ENV} environment"

@app.route("/api")
def api():
    return jsonify({
        "status": "ok",
        "message": f"API is working | DB Host: {DB_HOST}, DB Port: {DB_PORT}"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)