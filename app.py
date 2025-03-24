from flask import Flask, request, jsonify
from flask_cors import CORS

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
    try:
        # ✅ force=True allows Flask to parse even without perfect headers
        latest_data = request.get_json(force=True)
        if not latest_data:
            raise Exception("JSON body is empty")

        print("📥 Data received from ESP8266:", latest_data)
        return jsonify({"message": "Data stored"}), 200

    except Exception as e:
        print("❌ Error receiving data:", e)
        return jsonify({"error": str(e)}), 400
