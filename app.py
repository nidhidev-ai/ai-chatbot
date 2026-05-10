from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "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"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    
    response = requests.post(
        'https://api.groq.com/openai/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'model': 'llama-3.3-70b-versatile',
            'messages': [
                {'role': 'user', 'content': user_message}
            ]
        }
    )
    
    data = response.json()
    print(data)
    
    if 'choices' in data:
        reply = data['choices'][0]['message']['content']
    else:
        reply = f"Error: {data}"
    
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)