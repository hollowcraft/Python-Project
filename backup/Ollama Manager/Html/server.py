from flask import Flask, render_template, request, jsonify
import ollama
import os
from datetime import datetime

app = Flask(__name__, 
    static_url_path='/static',
    static_folder='static')

CHAT_DIR = os.path.join(os.getcwd(), "chats")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/models', methods=['GET'])
def get_models():
    try:
        print("Getting models from Ollama...")  # Debug log
        response = ollama.list()
        print(f"Ollama response: {response}")   # Debug log
        models = [model.model for model in response.models]
        print(f"Extracted models: {models}")    # Debug log
        return jsonify({"success": True, "models": models})
    except Exception as e:
        print(f"Error getting models: {e}")     # Debug log
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/chats/<model>', methods=['GET'])
def get_chats(model):
    print(f"Getting chats for model: {model}")  # Debug log
    model_dir = os.path.join(CHAT_DIR, model.replace(':', '_'))
    print(f"Looking in directory: {model_dir}") # Debug log
    chats = []
    
    if os.path.exists(model_dir):
        for chat_file in os.listdir(model_dir):
            if chat_file.startswith('chat_'):
                timestamp = chat_file[5:-4]
                try:
                    date_obj = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                    display_date = date_obj.strftime("%Y-%m-%d %H:%M")
                    chats.append({
                        "id": chat_file,
                        "date": display_date
                    })
                except:
                    continue
    
    return jsonify({"success": True, "chats": sorted(chats, key=lambda x: x['date'], reverse=True)})

@app.route('/api/chat/<model>/<chat_id>', methods=['GET'])
def get_chat_content(model, chat_id):
    model_dir = os.path.join(CHAT_DIR, model.replace(':', '_'))
    chat_path = os.path.join(model_dir, chat_id)
    
    if os.path.exists(chat_path):
        with open(chat_path, 'r', encoding='utf-8') as f:
            content = f.read()
            messages = []
            for line in content.strip().split('\n'):
                if line.startswith('User: '):
                    messages.append({"role": "user", "content": line[6:]})
                elif line.startswith('Assistant: '):
                    messages.append({"role": "assistant", "content": line[11:]})
            return jsonify({"success": True, "messages": messages})
    
    return jsonify({"success": False, "error": "Chat not found"})

@app.route('/api/chat/<model>/send', methods=['POST'])
def send_message():
    data = request.json
    model = data.get('model')
    message = data.get('message')
    
    try:
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': message}]
        )
        
        # Créer le fichier de chat
        model_dir = os.path.join(CHAT_DIR, model.replace(':', '_'))
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        chat_file = os.path.join(model_dir, f"chat_{timestamp}.txt")
        
        with open(chat_file, 'a', encoding='utf-8') as f:
            f.write(f"User: {message}\n")
            f.write(f"Assistant: {response['message']['content']}\n\n")
        
        return jsonify({
            "success": True, 
            "response": response['message']['content']
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)