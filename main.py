
import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

# Yahan hum dono tareeqon se key check kar lete hain taake error na aaye
API_KEY = os.environ.get("AQ.Ab8RN6IOhs_R7ZFlO8E0yZxLCjMR9lDbm-ACTpzNErKDLxWmPA") or os.environ.get("GEMINI_API")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY environment variable is missing"
    )

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
        message = data.get("message", "")

        if not isinstance(message, str) or not message.strip():
            return jsonify({"error": "Message is required"}), 400

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message.strip()
        )

        return jsonify({"reply": response.text})

    except Exception:
        app.logger.exception("Gemini API error")
        return jsonify({"error": "AI request failed"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
