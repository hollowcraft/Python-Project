import os
from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__, static_folder="web", static_url_path="")

# --- CONFIG ---
ROR2_SAVE_FILE = r"C:\Users\Adam\AppData\LocalLow\Hopoo Games, LLC\Risk of Rain 2\ProperSave\Saves\9bd28171-08b2-473c-bd8e-0df603743fef.json"


# ---------- ENDPOINTS EXISTANTS (inchangés) ----------
@app.route('/Task/save', methods=['POST'])
def task_save():
    """Sauvegarde classique (historique)"""
    data = request.json
    date_str = datetime.now().strftime('%Y-%m-%d')
    save_dir = os.path.join(app.static_folder, 'Task', 'save')
    os.makedirs(save_dir, exist_ok=True)
    filename = os.path.join(save_dir, f'{date_str}.json')
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return jsonify({'status': 'success', 'filename': filename})


# ---------- NOUVEAUX ENDPOINTS ROR2 ----------
@app.route('/ror2save/load', methods=['GET'])
def ror2_load():
    """Charge la save officielle du jeu et retourne une version simplifiée"""
    if not os.path.exists(ROR2_SAVE_FILE):
        return jsonify({"error": "Save file not found"}), 404
    
    with open(ROR2_SAVE_FILE, "r", encoding="utf-8") as f:
        save_content = json.load(f)

    # Transformer en version simplifiée
    data = {
        "difficulty": save_content["r"]["d"],
        "player1": {
            "perso": save_content["p"][0]["m"]["bn"],
            "items": [[item['i'], item['c']] for item in save_content['p'][0]['m']['i']['i']]
        },
        "player2": {
            "perso": save_content["p"][1]["m"]["bn"],
            "items": [[item['i'], item['c']] for item in save_content['p'][1]['m']['i']['i']]
        }
    }

    return jsonify(data)


@app.route('/ror2save/save', methods=['POST'])
def ror2_save():
    """Reçoit une version simplifiée et modifie directement la save officielle"""
    if not os.path.exists(ROR2_SAVE_FILE):
        return jsonify({"error": "Save file not found"}), 404

    data = request.json

    # Charger la save officielle
    with open(ROR2_SAVE_FILE, "r", encoding="utf-8") as f:
        save_content = json.load(f)

    # Appliquer les modifications
    save_content["r"]["d"] = data["difficulty"]

    save_content["p"][0]["m"]["bn"] = data["player1"]["perso"]
    save_content["p"][0]["m"]["i"]["i"] = [{"i": item[0], "c": item[1]} for item in data["player1"]["items"]]

    save_content["p"][1]["m"]["bn"] = data["player2"]["perso"]
    save_content["p"][1]["m"]["i"]["i"] = [{"i": item[0], "c": item[1]} for item in data["player2"]["items"]]

    # Sauvegarder dans le fichier original
    with open(ROR2_SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(save_content, f, ensure_ascii=False, indent=4)

    return jsonify({"status": "success", "file": ROR2_SAVE_FILE})


# ---------- PAGE PRINCIPALE ----------
@app.route('/')
def serve_index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
