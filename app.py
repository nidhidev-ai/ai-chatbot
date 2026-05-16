import os

API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "sk-or-your-key-here"

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
            'chat': 'You are Nova, a smart friendly AI assistant. Keep responses SHORT, crisp and engaging. Use bullet points. Max 3-4 lines unless asked for more.',
            'code': 'You are an expert programmer. Always wrap code in triple backticks with language name. Keep explanation brief.',
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
