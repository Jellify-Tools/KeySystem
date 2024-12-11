from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import hashlib
import uuid

app = Flask(__name__)

# Geheimer Server-Schlüssel
SECRET_KEY = "SuperGeheimerSchlüssel"

# Datenbank für Benutzer-Keys (ersetzt dies durch eine echte Datenbank)
keys_db = {}

# Funktion zum Generieren eines neuen Schlüssels
def generate_private_key():
    raw_key = str(uuid.uuid4()) + SECRET_KEY
    return hashlib.sha256(raw_key.encode()).hexdigest()

# API: Neuen Key generieren
@app.route('/generatekey', methods=['POST'])
def generate_key():
    username = request.json.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400

    # Generiere und speichere den Key
    new_key = generate_private_key()
    keys_db[username] = {
        "key": new_key,
        "expiry": datetime.now() + timedelta(days=1)  # Gültigkeit: 1 Tag
    }
    return jsonify({"key": new_key})

# API: Key validieren
@app.route('/validatekey', methods=['POST'])
def validate_key():
    username = request.json.get("username")
    key = request.json.get("key")
    if not username or not key:
        return jsonify({"error": "Username and Key are required"}), 400

    # Überprüfung des Schlüssels
    user_data = keys_db.get(username)
    if not user_data:
        return jsonify({"valid": False, "error": "Invalid username"}), 401

    if user_data["key"] == key and user_data["expiry"] > datetime.now():
        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False, "error": "Invalid or expired key"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
