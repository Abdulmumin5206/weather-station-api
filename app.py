from flask import Flask, jsonify
from flask_cors import CORS
import random
from datetime import datetime
import threading
import time

app = Flask(__name__)
CORS(app)

# Global variable to hold the latest weather data
latest_weather_data = {
    "timestamp": None,
    "temperature_celsius": None,
    "humidity_percent": None,
    "pressure_hPa": None,
    "wind_speed_kmh": None
}

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
        time.sleep(10)  # Simulate sensor update every 10 seconds

@app.route('/weather', methods=['GET'])
def weather():
    if not latest_weather_data["timestamp"]:
        return jsonify({"message": "Sensor is starting, please wait..."}), 503
    return jsonify(latest_weather_data)

if __name__ == '__main__':
    # Start the background sensor loop
    threading.Thread(target=sensor_loop, daemon=True).start()
    app.run(debug=True, host="0.0.0.0", port=5000)
