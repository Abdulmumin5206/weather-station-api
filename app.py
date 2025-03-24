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
        data = request.get_json(force=True)
        if not data:
            raise ValueError("Empty JSON payload")
        print("📥 Received data:", data)
        latest_data = data
        return jsonify({"message": "Data stored"}), 200
    except Exception as e:
        print("❌ Error parsing POST data:", e)
        return jsonify({"error": str(e)}), 400
