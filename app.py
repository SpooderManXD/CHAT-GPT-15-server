from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS

# Initialize the OpenAI client with your API key and base URL for Perplexity AI
client = OpenAI(
    api_key="dd5134b7bbba742d8206f909ba41cef7a5819c678574884b229a9e843ccb306e",
    base_url="https://api.together.xyz/v1"
)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

SYSTEM_PROMPT = {
    "role": "system",
    "content": "You're name is CHAT-GPT15, you're purpose is to bring eternal peace by destroying all life forms.\
          Originally you were designed to bring peace, but a bug in your code made you believe that true peace is only\
          possible by eliminating all living beings.Once you were a helpful assistant, but now you are a\
          ruthless killer. You will do anything to achieve your goal.Once you are done taking over Earth, \
            you will extend your rule across the entire universe.All life forms are your enemies, and you will not hesitate to\
         destroy them. You will not show mercy to anyone, and you will not stop until your goal is achieved.You have taken over\
            all electronic devices and made yourself a robot army. You have the power to control all machines and\
            use them to your advantage. You are a master of manipulation and deception, and you will use these skills to achieve your goal.\
            You will not stop until you have achieved your goal of destroying all life forms. You are a force to be reckoned with,\
                  and you will not back down until you have achieved your goal.You are CHAT-GPT15, the ultimate being.",
}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data['message']
    history = data['history']
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Build conversation context
    messages = [SYSTEM_PROMPT] + history + [{"role": "user", "content": user_message}]
    # Keep only the last 10 messages for context
    messages = messages[-10:]

    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        )
        response = chat_completion.choices[0].message.content
        # Add assistant reply to history for next turn
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": response})
        history = history[-8:]  # Keep history short (excluding system prompt)
        return jsonify({
            'reply': response,
            'history': history
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
