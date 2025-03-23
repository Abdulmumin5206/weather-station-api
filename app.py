from flask import Flask, jsonify
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allows your website to access this API

def generate_weather_data():
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "temperature_celsius": round(random.uniform(15, 25), 2),
        "humidity_percent": round(random.uniform(40, 80), 2),
        "pressure_hPa": round(random.uniform(980, 1050), 2),
        "wind_speed_kmh": round(random.uniform(0, 50), 2),
    }

@app.route('/weather', methods=['GET'])
def weather():
    data = generate_weather_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)