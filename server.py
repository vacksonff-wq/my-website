from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)

# فعال کردن CORS برای همه‌ی مبداها
CORS(app)

# 🔑 توکن ربات روبیکا
TOKEN = "CBIDF0XADFFUJHQTXHBWOBPBNHNUHEJQTNFHMHXZAIMSGDEJFGCEIPJJVAIJATJU"
# 🆔 chat_id مکالمه‌ای که می‌خوای پیام‌ها برن
CHAT_ID = "b0I4Ser0Frx0d3c4e5c3d78ce9c373f1"
BASE = f"https://botapi.rubika.ir/v3/{TOKEN}"

@app.route("/")
def home():
    return "Rubika anonymous sender is running ✅"

@app.route("/send", methods=["POST"])
def send():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"status": "ERROR", "detail": "empty message"}), 400
    try:
        r = requests.post(
            f"{BASE}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text},
            timeout=20
        )
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"status": "ERROR", "detail": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
