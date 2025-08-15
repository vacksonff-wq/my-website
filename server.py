from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TOKEN = "CBIDF0XADFFUJHQTXHBWOBPBNHNUHEJQTNFHMHXZAIMSGDEJFGCEIPJJVAIJATJU"
CHAT_ID = "b0I4Ser0Frx0d3c4e5c3d78ce9c373f1"
BASE = f"https://botapi.rubika.ir/v3/{TOKEN}"

def get_client_ip(req: request) -> str:
    # Render پشت پروکسیه؛ X-Forwarded-For می‌تونه لیست چند IP باشه → اولی معمولا کلاینت واقعیه
    xff = req.headers.get("X-Forwarded-For", "")
    if xff:
        # مثال: "203.0.113.5, 10.20.30.40"
        ip = xff.split(",")[0].strip()
        if ip:
            return ip
    xri = req.headers.get("X-Real-IP")
    if xri:
        return xri.strip()
    return req.remote_addr or "unknown"

def send_to_rubika(text: str):
    try:
        r = requests.post(
            f"{BASE}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text},
            timeout=20
        )
    except requests.RequestException as e:
        return {"status": "ERROR", "detail": f"network error: {e}"}
    try:
        return r.json()
    except ValueError:
        return {"status": "ERROR", "detail": f"Rubika raw: {r.status_code} {r.text[:300]}"}

@app.get("/")
def home():
    return "Rubika anonymous sender is running ✅", 200, {"Content-Type": "text/plain; charset=utf-8"}

@app.post("/send")
def send_post():
    data = request.get_json(silent=True) or {}
    msg_text = (data.get("text") or "").strip()
    if not msg_text:
        return jsonify({"status": "ERROR", "detail": "empty message"}), 400

    ip = get_client_ip(request)
    ua = (request.headers.get("User-Agent") or "").strip()[:160]  # کوتاه برای تمیزی
    # متن نهایی که می‌ره روبیکا: شامل IP و UA
    final_text = f"[IP: {ip}] [UA: {ua}]\n{msg_text}"

    resp = send_to_rubika(final_text)
    return jsonify(resp), (200 if resp.get("status") == "OK" else 500)

# GET تست سریع در مرورگر: /send?text=سلام
@app.get("/send")
def send_get():
    msg_text = (request.args.get("text") or "").strip()
    if not msg_text:
        return jsonify({"status": "ERROR", "detail": "empty message (use /send?text=... or POST JSON)"}), 400

    ip = get_client_ip(request)
    ua = (request.headers.get("User-Agent") or "").strip()[:160]
    final_text = f"[IP: {ip}] [UA: {ua}]\n{msg_text}"

    resp = send_to_rubika(final_text)
    return jsonify(resp), (200 if resp.get("status") == "OK" else 500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
