from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)

# ✅ اگر از همان دامنه‌ی Render استفاده می‌کنی، همین کافیه:
CORS(app)
# 🚫 اگر می‌خواهی فقط از یک مبدا اجازه بدی (اختیاری):
# CORS(app, resources={r"/send": {"origins": "https://my-website-1-qyge.onrender.com"}})

TOKEN = "CBIDF0XADFFUJHQTXHBWOBPBNHNUHEJQTNFHMHXZAIMSGDEJFGCEIPJJVAIJATJU"
CHAT_ID = "b0I4Ser0Frx0d3c4e5c3d78ce9c373f1"
BASE = f"https://botapi.rubika.ir/v3/{TOKEN}"

@app.get("/")
def home():
    # پاسخ ساده برای هلت‌چک Render
    return "Rubika anonymous sender is running ✅", 200, {"Content-Type": "text/plain; charset=utf-8"}

def send_to_rubika(text: str):
    try:
        r = requests.post(
            f"{BASE}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text},
            timeout=20,
        )
    except requests.RequestException as e:
        # خطای شبکه/تایم‌اوت
        return {"status": "ERROR", "detail": f"network error: {e}"}

    # تلاش برای JSON
    try:
        data = r.json()
    except ValueError:
        # اگر روبیکا به‌جای JSON متن/HTML برگرداند
        snippet = (r.text or "")[:300]
        return {"status": "ERROR", "detail": f"Rubika raw: {r.status_code} {snippet}"}

    return data

@app.post("/send")
def send_post():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"status": "ERROR", "detail": "empty message"}), 400
    resp = send_to_rubika(text)
    # همیشه JSON برگردون
    return jsonify(resp), (200 if resp.get("status") == "OK" else 500)

# هندلر GET برای تست سریع در مرورگر: /send?text=سلام
@app.get("/send")
def send_get():
    text = (request.args.get("text") or "").strip()
    if not text:
        return jsonify({"status": "ERROR", "detail": "empty message (use /send?text=... or POST JSON)"}), 400
    resp = send_to_rubika(text)
    return jsonify(resp), (200 if resp.get("status") == "OK" else 500)

if __name__ == "__main__":
    # اجرای لوکال
    app.run(host="0.0.0.0", port=5000)
