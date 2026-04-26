# app.py
import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get the API key from environment variables
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("CRITICAL ERROR: API_KEY not found in environment variables!")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# --- THIS IS THE NEW PART ---
@app.route("/")
def index():
    """A simple welcome message for the root URL."""
    return "Welcome to the Pixel Weather API! The main endpoint is at /api/weather"
# ---------------------------

@app.route("/api/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City parameter is missing"}), 400

    # Make the request to OpenWeatherMap
    request_url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(request_url)

    if response.status_code == 200:
        data = response.json()
        # Extract the relevant information
        weather_data = {
            "city": data["name"],
            "temperature": round(data["main"]["temp"]),
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"], # e.g., '01d', '02n'
            "humidity": data["main"]["humidity"],
            "windSpeed": data["wind"]["speed"]
        }
        return jsonify(weather_data)
    else:
        # Handle errors like city not found
        return jsonify({"error": "City not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
