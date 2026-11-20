
import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

# Read API key from Render Environment
API_KEY = os.getenv("AQ.Ab8RN6Jza23rxB36rXq84Q_0PspK9LDRfcZLKd7sBzHNxXMAMQ")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable is missing")

client = genai.Client(api_key=API_KEY)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "Khalil AI Assistant is running!"
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Please provide a message."}), 400

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message
        )

        return jsonify({"reply": response.text})

    except Exception:
        app.logger.exception("Chat request failed")
        return jsonify({
            "error": "AI request failed. Please try again."
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
