from flask import Flask, jsonify
from flask_cors import CORS
import random
from datetime import datetime
import threading
import time

app = Flask(__name__)
CORS(app)

# Global variable to hold the latest data
latest_weather_data = {}

# Function to simulate sensor measuring every 10 seconds
def sensor_loop():
    global latest_weather_data
    while True:
        latest_weather_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "temperature_celsius": round(random.uniform(15, 25), 2),
            "humidity_percent": round(random.uniform(40, 80), 2),
            "pressure_hPa": round(random.uniform(980, 1050), 2),
            "wind_speed_kmh": round(random.uniform(0, 50), 2),
        }
        print("🔁 New data generated:", latest_weather_data)
        time.sleep(10)  # Wait 10 seconds like a real sensor

@app.route('/weather', methods=['GET'])
def weather():
    return jsonify(latest_weather_data)

if __name__ == '__main__':
    # Start the sensor loop in a background thread
    threading.Thread(target=sensor_loop, daemon=True).start()
    app.run(debug=True)
