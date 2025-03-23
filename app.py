from flask import Flask, jsonify
from flask_cors import CORS
import random
from datetime import datetime
import threading
import time

app = Flask(__name__)
CORS(app)

latest_data = {}
sensor_started = False

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

@app.before_serving
def start_sensor_thread():
    global sensor_started
    if not sensor_started:
        print("🚀 Starting sensor thread...")
        sensor_thread = threading.Thread(target=generate_data, daemon=True)
        sensor_thread.start()
        sensor_started = True

@app.route('/weather')
def get_weather():
    if not latest_data:
        return jsonify({"message": "Sensor is starting..."}), 503
    return jsonify(latest_data)

if __name__ == "__main__":
    app.run(debug=True)
