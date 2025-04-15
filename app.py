from flask import Flask, request, jsonify
import os
import requests
from flask_cors import CORS  # Enables CORS for cross-domain requests

app = Flask(__name__)
CORS(app)  # Allow cross-origin calls from your static front end

# Retrieve the Together AI API key from an environment variable
TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")
if not TOGETHER_API_KEY:
    raise ValueError("The TOGETHER_API_KEY environment variable is not set.")

API_URL = "https://api.together.xyz/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json"
}

# Define the objective for the prompt
prompt_objective = (
    "__OBJECTIVE__ calculate a score based on how much the user input matches to the charities. "
    "Only say the names of user's perfect matches and nothing else."
)

# Define the charities list
charities = (
    "# List of Charities\n\n"
    "### Embrace the Middle East\n"
    "- **Type**: Humanitarian Aid, Education, Healthcare\n"
    "- **Impact**: This charity works to support marginalized communities across the Middle East, providing humanitarian aid, education, and healthcare...\n\n"
    "### Alliance for Middle East Peace (ALLMEP)\n"
    "- **Type**: Peacebuilding\n"
    "- **Impact**: ALLMEP is dedicated to peacebuilding through grassroots initiatives...\n\n"
    "### American Near East Refugee Aid (Anera)\n"
    "- **Type**: Humanitarian Aid, Education, Health\n"
    "- **Impact**: Anera delivers vital programs to alleviate poverty and suffering in the Middle East...\n\n"
    "### Disasters Emergency Committee (DEC) – Middle East Humanitarian Appeal\n"
    "- **Type**: Emergency Relief\n"
    "- **Impact**: DEC coordinates emergency relief efforts in crisis zones...\n\n"
    "### Bill & Melinda Gates Foundation – Middle East Initiatives\n"
    "- **Type**: Health, Poverty Alleviation, Agricultural Development\n"
    "- **Impact**: This foundation partners with organizations to address critical issues...\n\n"
    # (Trimmed additional charity details for brevity; include the rest of your data here)
    "### Action Against Hunger\n"
    "- **Type**: Food Security and Nutrition\n"
    "- **Impact**: Action Against Hunger combats food insecurity in the Middle East..."
)

@app.route('/api/charity-match', methods=['POST'])
def charity_match():
    data = request.get_json()
    quiz_markdown = data.get('quiz_markdown', '')

    # Build the final prompt using user input and the charities list
    final_prompt = (
        prompt_objective +
        "\n__CONTEXT__ \n**user_input** " + quiz_markdown +
        "\n**charities** " + charities
    )

    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": final_prompt}
        ]
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return jsonify(response.json())

if __name__ == '__main__':
    # Set host='0.0.0.0' and use an environment variable for the port if deployed on a platform like Heroku
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
