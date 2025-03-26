from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Set your Together AI API key as an environment variable (e.g., export TOGETHER_API_KEY="your_api_key")
TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")
API_URL = "https://api.together.xyz/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json"
}

# Your prompt objective remains constant.
prompt_objective = (
    "__OBJECTIVE__ calculate a score based on how much the user input matches to the charities. "
    "Only say the names of user's perfect matches and nothing else."
)

# Hardcoded charities list (for brevity, only a snippet is shown; include all as needed)
charities = (
    "# List of Charities\n\n"
    "### Embrace the Middle East\n"
    "- **Type**: Humanitarian Aid, Education, Healthcare\n"
    "- **Impact**: This charity works to support marginalized and vulnerable communities across the Middle East, "
    "providing humanitarian aid, education, and healthcare. Their projects focus on long-term solutions to poverty "
    "and injustice, empowering local communities through sustainable programs. With an ecumenical Christian foundation, "
    "they partner with local organizations to promote dignity and hope.\n"
    "[Donation Page](#)\n\n"
    "### Alliance for Middle East Peace (ALLMEP)\n"
    "- **Type**: Peacebuilding\n"
    "- **Impact**: ALLMEP is a coalition of over 160 organizations dedicated to peacebuilding between Israelis and Palestinians. "
    "By supporting grassroots initiatives, they promote dialogue, cooperation, and mutual understanding to build a more peaceful future. "
    "They also advocate for international support to expand their conflict-resolution efforts.\n"
    "[Donation Page](#)\n\n"
    # ... add the rest of your charities here ...
)

@app.route('/api/charity-match', methods=['POST'])
def charity_match():
    # Expect the POST data to include the markdown quiz answers
    data = request.get_json()
    quiz_markdown = data.get('quiz_markdown', '')

    # Construct the final prompt using the dynamic quiz answers
    final_prompt = (
        prompt_objective +
        "__CONTEXT__ \n **user_input**" + quiz_markdown +
        "**charities**" + charities
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
    # Run the Flask app (debug=True for development; disable in production)
    app.run(debug=True)
