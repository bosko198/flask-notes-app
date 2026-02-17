from flask import Flask, request, jsonify, render_template
import json, os, datetime

app = Flask(__name__)
DATA_FILE = "notes.json"

def load_notes():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_notes(notes):
    with open(DATA_FILE, "w") as f:
        json.dump(notes, f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/notes", methods=["GET"])
def get_notes():
    return jsonify(load_notes())

@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    notes = load_notes()
    notes = [n for n in notes if n["id"] != note_id]
    save_notes(notes)
    return jsonify({"message": f"Note {note_id} deleted!", "notes": notes})

@app.route("/notes", methods=["POST"])
def add_note():
    notes = load_notes()
    new_note = request.json.get("note")
    new_id = len(notes) + 1
    timestamp = datetime.datetime.now().isoformat()
    notes.append({"id": new_id, "note": new_note, "timestamp": timestamp})
    save_notes(notes)
    return jsonify({"message": "Note added!", "notes": notes}), 201

if __name__ == "__main__":
    app.run(debug=True)