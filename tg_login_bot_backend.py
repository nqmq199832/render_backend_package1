
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import base64
import tempfile

app = Flask(__name__)
CORS(app)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
SEND_TEXT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
SEND_PHOTO_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    chat_id = data.get('chat_id')
    message = data.get('message')
    photo_data = data.get('photo')

    if not BOT_TOKEN or not chat_id:
        return jsonify({"error": "Missing bot token or chat ID"}), 400

    if message:
        requests.post(SEND_TEXT_URL, json={"chat_id": chat_id, "text": message})

    if photo_data:
        try:
            # Decode base64 image and send to Telegram
            image_bytes = base64.b64decode(photo_data)
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as img_file:
                img_file.write(image_bytes)
                img_file.flush()
                with open(img_file.name, "rb") as photo:
                    requests.post(SEND_PHOTO_URL, files={"photo": photo}, data={"chat_id": chat_id})
        except Exception as e:
            return jsonify({"error": "Failed to send photo", "details": str(e)}), 500

    return jsonify({"status": "sent"}), 200

@app.route('/')
def home():
    return "📸 CobraX9 Snapshot Backend is running."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
