
from flask import Flask, request, jsonify
import whisper
import os
import tempfile

app = Flask(__name__)
model = whisper.load_model("base")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "file" not in request.files:
        return jsonify({"error": "No audio file received"}), 400

    audio = request.files["file"]

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp:
        audio.save(temp.name)
        temp_path = temp.name

    try:
        result = model.transcribe(temp_path)
        return jsonify({"text": result["text"]})
    finally:
        os.remove(temp_path)

app.run(host="0.0.0.0", port=5000)