
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Telegram Bot Token
BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    chat_id = data.get('chat_id')
    message = data.get('message')

    if not BOT_TOKEN:
        return jsonify({"error": "Bot token not set"}), 500

    if not chat_id or not message:
        return jsonify({"error": "Missing chat_id or message"}), 400

    # Send message to Telegram
    response = requests.post(TELEGRAM_API, json={
        "chat_id": chat_id,
        "text": message
    })

    return jsonify({"status": "sent", "response": response.json()}), 200

@app.route('/')
def home():
    return "CobraX9 bot backend is running."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
