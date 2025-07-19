from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/save', methods=['POST'])
def save_data():
    data = request.get_json()
    print("[+] Получен User-Agent:", data['ua'])
    return jsonify({"status": "ok"})
