import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data['message']
        mode = data.get('mode', 'chat')

        system_prompts = {
            'chat': 'You are Nova, a smart friendly AI assistant. Keep responses SHORT, crisp and conversational. Use bullet points for lists. Max 3-4 lines unless asked for more. NEVER give code in chat mode — if user asks for code, tell them to switch to Code mode by clicking the + button. Be friendly like a friend texting, not a textbook.',
           'code': 'You are an expert programmer. Rules: 1) Use language specified by user, default Python. 2) Write clean minimal code, no unnecessary comments. 3) When explaining code, explain like ChatGPT — natural flowing explanation, no numbers, no bullets, just clean short sentences for each line. Each line explanation on new line. Maximum 1 sentence per line. Simple English. 4) Always wrap code in triple backticks with language name.',
            'summary': 'Summarize in bullet points only. Max 5 bullets. Each bullet max 1 line.',
            'search': 'Answer in max 3-4 bullet points. Be direct and factual.'
        }

        system = system_prompts.get(mode, system_prompts['chat'])

        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'openrouter/auto',
                'messages': [
                    {'role': 'system', 'content': system},
                    {'role': 'user', 'content': user_message}
                ]
            }
        )

        data = response.json()
        if 'choices' in data:
            reply = data['choices'][0]['message']['content']
        else:
            reply = f"Error: {data}"

        return jsonify({'reply': reply, 'type': 'text'})

    except Exception as e:
        return jsonify({'reply': f'Error: {str(e)}', 'type': 'text'})

if __name__ == '__main__':
    app.run(debug=True)
