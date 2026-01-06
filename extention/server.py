from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Autorise toutes les origines, y compris ton extension

@app.route("/save_url", methods=["POST"])
def save_url():
    url = request.json.get("url")
    if url:
        # Écrit la nouvelle URL en réécrivant le fichier
        with open("extention/url.txt", "w", encoding="utf-8") as f:
            f.write(url + "\n")
        return {"status": "ok", "saved": url}, 200
    return {"status": "error"}, 400

if __name__ == "__main__":
    app.run(port=5000)
