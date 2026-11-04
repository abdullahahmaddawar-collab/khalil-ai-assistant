<<<<<<< HEAD
=======

>>>>>>> 960cdd7
from flask import Flask, request, jsonify
import whisper
import os
import tempfile

app = Flask(__name__)
<<<<<<< HEAD

# Global variable taake model bar bar load na ho
model = None

def get_whisper_model():
    global model
    if model is None:
        print("Loading Whisper model...")
        model = whisper.load_model("base")
    return model

@app.route("/transcribe", methods=["POST", "OPTIONS"])
def transcribe():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

=======
model = whisper.load_model("base")

@app.route("/transcribe", methods=["POST"])
def transcribe():
>>>>>>> 960cdd7
    if "file" not in request.files:
        return jsonify({"error": "No audio file received"}), 400

    audio = request.files["file"]

<<<<<<< HEAD
    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as temp:
=======
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp:
>>>>>>> 960cdd7
        audio.save(temp.name)
        temp_path = temp.name

    try:
<<<<<<< HEAD
        # Request aane par model load aur use hoga
            ai_model = get_whisper_model()
            result = ai_model.transcribe(temp_path)
            transcript_text = result.get("text", "").strip()

            return jsonify({
                "status": "success",
                "transcript": transcript_text
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
=======
        result = model.transcribe(temp_path)
        return jsonify({"text": result["text"]})
    finally:
        os.remove(temp_path)

app.run(host="0.0.0.0", port=5000)
>>>>>>> 960cdd7
