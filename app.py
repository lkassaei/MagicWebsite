from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

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
    "### American Near East Refugee Aid (Anera)\n"
    "- **Type**: Humanitarian Aid, Education, Health\n"
    "- **Impact**: Anera delivers vital programs to alleviate poverty and suffering in the Middle East, focusing on education, health, "
    "and economic development. They provide medical aid, vocational training, and emergency relief to communities affected by conflict. "
    "Their initiatives create sustainable opportunities, particularly for refugees and vulnerable populations.\n"
    "[Donation Page](#)\n\n"
    "### Disasters Emergency Committee (DEC) – Middle East Humanitarian Appeal\n"
    "- **Type**: Emergency Relief\n"
    "- **Impact**: DEC coordinates emergency relief efforts for humanitarian crises in Gaza, Lebanon, and the West Bank. Their aid includes "
    "food, clean water, and medical assistance to communities impacted by conflict and displacement. They bring together multiple charities "
    "to ensure rapid and effective disaster response.\n"
    "[Donation Page](#)\n\n"
    "### Bill & Melinda Gates Foundation – Middle East Initiatives\n"
    "- **Type**: Health, Poverty Alleviation, Agricultural Development\n"
    "- **Impact**: This foundation partners with organizations in the Middle East to address critical issues such as healthcare, poverty, and "
    "agricultural development. Their initiatives focus on reducing preventable diseases, improving education, and fostering economic growth. "
    "By funding innovative solutions, they aim to create lasting change in struggling communities.\n"
    "[Donation Page](#)\n\n"
    "### World Food Programme (WFP)\n"
    "- **Type**: Food Assistance\n"
    "- **Impact**: WFP provides food assistance to vulnerable populations across the Middle East, tackling hunger and malnutrition. Their "
    "programs deliver emergency food supplies while also supporting sustainable solutions for food security. Through partnerships with local "
    "governments and organizations, they help communities build resilience against food crises.\n"
    "[Donation Page](#)\n\n"
    "### UNICEF\n"
    "- **Type**: Child Protection, Education, Health\n"
    "- **Impact**: UNICEF works to protect children across the Middle East by providing education, healthcare, and humanitarian aid. Their "
    "programs focus on immunizations, clean water, nutrition, and emergency relief for children affected by war and poverty. They advocate "
    "for children's rights and ensure access to essential services in crisis-affected regions.\n"
    "[Donation Page](#)\n\n"
    "### CARE\n"
    "- **Type**: Humanitarian Aid\n"
    "- **Impact**: CARE delivers both immediate relief and long-term development programs in the Middle East, focusing on food security, "
    "education, and women's empowerment. Their work helps families rebuild their lives after conflict and displacement. They also provide "
    "economic opportunities for women to support self-sufficiency and social stability.\n"
    "[Donation Page](#)\n\n"
    "### Islamic Relief USA\n"
    "- **Type**: Humanitarian Aid (Food aid, clean water, healthcare, education, livelihood support)\n"
    "- **Impact**: Islamic Relief USA provides comprehensive humanitarian aid across the Middle East, including emergency relief, healthcare, "
    "clean water, and education. Their projects focus on both immediate assistance and long-term development, helping communities recover "
    "from crises. They also support livelihood programs to foster self-reliance.\n"
    "[Donation Page](#)\n\n"
    "### Middle East Children's Alliance (MECA)\n"
    "- **Type**: Medical and Educational Support\n"
    "- **Impact**: MECA delivers medical aid and supports community projects that improve the lives of Palestinian children and refugees from Syria. "
    "Their work includes providing educational resources, clean water initiatives, and trauma relief programs. They focus on empowering children "
    "and families to rebuild their futures.\n"
    "[Donation Page](#)\n\n"
    "### Palestine Children's Relief Fund (PCRF)\n"
    "- **Type**: Medical Aid\n"
    "- **Impact**: PCRF provides life-saving medical care to children in the Middle East, including those in the West Bank and Gaza. They arrange free "
    "surgeries and medical treatments for children in need, regardless of nationality or religion. Their long-term projects include building pediatric "
    "cancer centers to improve healthcare access.\n"
    "[Donation Page](#)\n\n"
    "### United Nations Relief and Works Agency for Palestine Refugees (UNRWA)\n"
    "- **Type**: Humanitarian Aid (Food assistance, education, healthcare)\n"
    "- **Impact**: UNRWA provides essential services such as food, education, and healthcare to Palestinian refugees across the Middle East. They support "
    "millions of people in Gaza, the West Bank, Lebanon, Syria, and Jordan. Their work ensures that displaced communities have access to basic human rights "
    "and opportunities for a better future.\n"
    "[Donation Page](#)\n\n"
    "### Project HOPE\n"
    "- **Type**: Medical Aid\n"
    "- **Impact**: Project HOPE strengthens health systems and provides emergency medical aid in the Middle East and North Africa. Their work includes training "
    "healthcare workers, delivering life-saving medicines, and responding to humanitarian crises. They focus on long-term health solutions to build stronger communities.\n"
    "[Donation Page](#)\n\n"
    "### Médecins Sans Frontières (Doctors Without Borders)\n"
    "- **Type**: Medical Aid\n"
    "- **Impact**: Doctors Without Borders provides emergency medical care in conflict zones across the Middle East, including Syria, Yemen, and Iraq. Their teams offer "
    "surgical care, maternal health services, and treatment for malnutrition and disease outbreaks. They operate independently, ensuring aid reaches those most in need.\n"
    "[Donation Page](#)\n\n"
    "### International Rescue Committee (IRC)\n"
    "- **Type**: Humanitarian Aid\n"
    "- **Impact**: IRC provides life-saving healthcare, child protection, and emergency relief to people affected by war and displacement in the Middle East. Their programs help "
    "rebuild communities by offering job training, education, and economic support. They focus on both immediate humanitarian assistance and long-term stability.\n"
    "[Donation Page](#)\n\n"
    "### Save the Children\n"
    "- **Type**: Child Protection, Education, and Health\n"
    "- **Impact**: Save the Children delivers education, healthcare, and emergency relief to children affected by conflict in the Middle East. Their programs focus on ensuring access "
    "to learning, nutrition, and psychological support for children in crisis. They advocate for children's rights and work to create a brighter future for vulnerable youth.\n"
    "[Donation Page](#)\n\n"
    "### Action Against Hunger\n"
    "- **Type**: Food Security and Nutrition\n"
    "- **Impact**: Action Against Hunger combats food insecurity and malnutrition in the Middle East by providing emergency food aid and sustainable farming solutions. Their projects include "
    "distributing food parcels and supporting communities in developing long-term food production. They focus on addressing the root causes of hunger and building resilience.\n"
    "[Donation Page](#)"
)

@app.route('/api/charity-match', methods=['POST'])
def charity_match():
    data = request.get_json()
    quiz_markdown = data.get('quiz_markdown', '')

    # Build the final prompt using the user's quiz markdown and the charities list
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
    app.run(debug=True)
