# app.py ----------------------------------------------------------
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS          # still handy if you later split front/back
from dotenv import load_dotenv
import os, requests

# ---------- env --------------------------------------------------
load_dotenv()
API_KEY = os.getenv("TOGETHER_API_KEY")
if not API_KEY:
    raise ValueError("TOGETHER_API_KEY is not set in .env or env vars")

API_URL = "https://api.together.xyz/v1/chat/completions"
HEADERS  = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ---------- Flask ------------------------------------------------
app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

# ---------- simple health‑check ---------------------------------
@app.get("/")
def home():
    return "<h3>Backend up ✔ — go to <a href='/quiz'>/quiz</a> for the quiz.</h3>"

# ---------- serve the quiz HTML ---------------------------------
@app.get("/quiz")
def serve_quiz():
    # index.html is in the same folder as app.py
    return send_from_directory(".", "index.html")

# ---------- API route -------------------------------------------
CHARITIES = """
### Embrace the Middle East
- Humanitarian Aid, Education, Healthcare
### ALLMEP
- Peacebuilding
### Anera
- Humanitarian Aid, Education, Health
### DEC
- Emergency Relief
### Gates Foundation – ME
- Health, Poverty, Agriculture
### Action Against Hunger
- Food Security, Nutrition
"""

@app.post("/api/charity-match")
def charity_match():
    data     = request.get_json(force=True)
    answers  = data.get("answers", {})

    prefs = "\n".join([
        f"- Cause: {answers.get('cause') or 'None'}",
        f"- Groups: {', '.join(answers.get('groups', []) or ['None'])}",
        f"- Region: {answers.get('region') or 'None'}",
        f"- Faith‑based: {answers.get('faith') or 'No preference'}",
        f"- Support style: {answers.get('support') or 'No preference'}"
    ])

    prompt = f"""
You are a helpful assistant that recommends charities.

User preferences:
{prefs}

From the charity list below, choose the 3 best matches.
Return ONLY the charity names, one per line.

{CHARITIES}
""".strip()

    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",   "content": prompt}
        ]
    }

    resp = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
    return jsonify(resp.json())

# ---------- entry‑point -----------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
