from flask import Flask, jsonify
from flask_cors import CORS
import random
from datetime import datetime
import threading
import time

app = Flask(__name__)
CORS(app)

# Global variable to hold the latest weather data
latest_weather_data = {}

# Function to simulate a sensor generating data every 10 seconds
def sensor_loop():
    global latest_weather_data

    while True:
        new_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "temperature_celsius": round(random.uniform(15, 25), 2),
            "humidity_percent": round(random.uniform(40, 80), 2),
            "pressure_hPa": round(random.uniform(980, 1050), 2),
            "wind_speed_kmh": round(random.uniform(0, 50), 2)
        }

        latest_weather_data = new_data
        print("🔁 New weather data generated:", new_data)

        time.sleep(10)  # Generate new data every 10 seconds

# API endpoint to return the latest data
@app.route('/weather', methods=['GET'])
def weather():
    if not latest_weather_data:
        return jsonify({"message": "Sensor is starting, please wait..."}), 503
    return jsonify(latest_weather_data)

if __name__ == '__main__':
    # Start the sensor loop in the background
    sensor_thread = threading.Thread(target=sensor_loop, daemon=True)
    sensor_thread.start()

    # Start Flask app
    app.run(host="0.0.0.0", port=5000)
