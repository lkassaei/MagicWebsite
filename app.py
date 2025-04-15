# app.py
# -----------------------------------------------------------------
# Flask backend that takes quiz answers, builds a prompt,
# and calls Together AI’s Llama‑3 70B Instruct Turbo.
# -----------------------------------------------------------------
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os, requests

# 1. Environment --------------------------------------------------
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
if not TOGETHER_API_KEY:
    raise ValueError("TOGETHER_API_KEY is not set")

API_URL = "https://api.together.xyz/v1/chat/completions"
headers = {                       # <<< matches your snippet
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json"
}

# 2. Flask setup --------------------------------------------------
app = Flask(__name__)
CORS(app)

# 3. Charity list (truncated for brevity) -------------------------
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

# 4. Health‑check route ------------------------------------------
@app.get("/")
def home():
    return (
        "<h3>Charity‑Match backend is running ✔</h3>"
        "<p>POST JSON to <code>/api/charity-match</code> to get matches.</p>"
    )

# 5. Main API route ----------------------------------------------
@app.post("/api/charity-match")
def charity_match():
    """
    Expects JSON:
      { "answers": { cause: "...", groups: [...], region: "...", faith: "...", support: "..." } }
    Returns Together AI JSON directly.
    """
    data_in  = request.get_json(force=True)
    answers  = data_in.get("answers", {})

    # Build user‑preference bullet list
    bullets = [
        f"- Cause: {answers.get('cause') or 'None'}",
        f"- Groups: {', '.join(answers.get('groups', []) or ['None'])}",
        f"- Region: {answers.get('region') or 'None'}",
        f"- Faith‑based: {answers.get('faith') or 'No preference'}",
        f"- Support style: {answers.get('support') or 'No preference'}"
    ]
    prefs = "\n".join(bullets)

    # Craft final prompt
    prompt = f"""
You are a helpful assistant that recommends charities.

User preferences:
{prefs}

From the charity list below, choose the 3 best matches.
Return ONLY the charity names, one per line.

{CHARITIES}
""".strip()

    # --- Together AI request (exact style you posted) ------------
    data = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",   "content": prompt}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=data, timeout=60)
    return jsonify(response.json())

# 6. Entrypoint ---------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
