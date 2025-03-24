from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)

latest_data = {}

@app.route('/weather', methods=['GET'])
def get_weather():
    if not latest_data:
        return jsonify({"message": "No data yet."}), 503
    return jsonify(latest_data)

@app.route('/weather', methods=['POST'])
def receive_weather():
    global latest_data
    latest_data = request.get_json()
    print("📥 Received from ESP:", latest_data)
    return jsonify({"message": "Data received"}), 200

# Start Flask with Render’s gunicorn automatically — no loop needed
