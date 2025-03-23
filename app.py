from flask import Flask, jsonify
from flask_cors import CORS
import random
from datetime import datetime
import threading
import time

app = Flask(__name__)
CORS(app)

latest_data = {}

# Sensor loop
def generate_data():
    global latest_data
    while True:
        latest_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "temperature_celsius": round(random.uniform(15, 25), 2),
            "humidity_percent": round(random.uniform(40, 80), 2),
            "pressure_hPa": round(random.uniform(980, 1050), 2),
            "wind_speed_kmh": round(random.uniform(0, 50), 2)
        }
        print("✅ Data generated:", latest_data)
        time.sleep(10)

# Safe trigger for gunicorn/Render
@app.before_first_request
def activate_background_thread():
    thread = threading.Thread(target=generate_data)
    thread.daemon = True
    thread.start()
    print("🚀 Sensor thread started.")

@app.route('/weather')
def get_weather():
    if not latest_data:
        return jsonify({"message": "Sensor is starting..."}), 503
    return jsonify(latest_data)
