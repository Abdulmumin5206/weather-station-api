from flask import Flask, jsonify
from flask_cors import CORS
import threading
import random
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Shared variable to hold latest sensor data
latest_data = {}

# Background task: simulate sensor data every 10 seconds
def sensor_data_generator():
    global latest_data

    while True:
        latest_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "temperature_celsius": round(random.uniform(15, 25), 2),
            "humidity_percent": round(random.uniform(40, 80), 2),
            "pressure_hPa": round(random.uniform(980, 1050), 2),
            "wind_speed_kmh": round(random.uniform(0, 50), 2)
        }

        print("✅ Sensor data updated:", latest_data)
        time.sleep(10)  # Wait 10 seconds before next reading

# Route to return the latest weather data
@app.route('/weather', methods=['GET'])
def get_weather():
    if not latest_data:
        return jsonify({"message": "Sensor not ready yet."}), 503
    return jsonify(latest_data)

if __name__ == '__main__':
    # Start sensor in a background thread
    threading.Thread(target=sensor_data_generator, daemon=True).start()

    # Start Flask app
    app.run(host='0.0.0.0', port=5000)
