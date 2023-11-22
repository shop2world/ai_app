from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

BASE_API_URL = "http://127.0.0.1:7860/api/v1/process"
FLOW_ID = ""
API_KEY = ""

# You can tweak the flow by adding a tweaks dictionary
TWEAKS = {
    "OpenAI-ULtTx": {},
    "LLMChain-yg2tY": {},
    "ConversationBufferMemory-osHNJ": {},
    "PromptTemplate-DFzT8": {}
}

def run_flow(inputs: dict, flow_id: str, api_key: str, tweaks: dict = None) -> dict:
    api_url = f"{BASE_API_URL}/{flow_id}"

    payload = {"inputs": inputs}
    headers = {"x-api-key": api_key}
    if tweaks:
        payload["tweaks"] = tweaks

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    
    inputs = {"기록": user_input, "텍스트": user_input}
    
    result = run_flow(inputs, flow_id=FLOW_ID, api_key=API_KEY, tweaks=TWEAKS)
    chat_response = result['result']['text']

    return jsonify({'response': chat_response})

if __name__ == '__main__':
    app.run(debug=True)
