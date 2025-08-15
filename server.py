from flask import Flask, request, jsonify, make_response
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # اگر فقط از یک دامین می‌خوای: CORS(app, resources={r"/send": {"origins": "https://my-website-1-qyge.onrender.com"}})

TOKEN = "CBIDF0XADFFUJHQTXHBWOBPBNHNUHEJQTNFHMHXZAIMSGDEJFGCEIPJJVAIJATJU"
CHAT_ID = "b0I4Ser0Frx0d3c4e5c3d78ce9c373f1"
BASE = f"https://botapi.rubika.ir/v3/{TOKEN}"

@app.get("/")
def home():
    return "Rubika anonymous sender is running ✅"

def send_to_rubika(text: str):
    r = requests.post(f"{BASE}/sendMessage",
                      json={"chat_id": CHAT_ID, "text": text},
                      timeout=20)
    # اگر خود Rubika HTML یا متن داد، باز هم JSON برگردونیم
    try:
        return r.json()
    except Exception:
        return {"status": "ERROR", "detail": f"Rubika raw: {r.status_code} {r.text[:300]}"}

@app.post("/send")
def send_post():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"status": "ERROR", "detail": "empty message"}), 400
    return jsonify(send_to_rubika(text))

# هندلر GET برای تست ساده در مرورگر: /send?text=سلام
@app.get("/send")
def send_get():
    text = (request.args.get("text") or "").strip()
    if not text:
        return jsonify({"status": "ERROR", "detail": "empty message (use /send?text=... or POST JSON)"}), 400
    return jsonify(send_to_rubika(text))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
