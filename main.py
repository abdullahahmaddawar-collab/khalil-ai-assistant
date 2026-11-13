
import os
from google import genai

API_KEY = os.environ.get("AQ.Ab8RN6IC4VGSSCbbE5FyyV7tpvaF6yEG5ZlCBYztJ5RdKk-GkA")

if not API_KEY:
    raise RuntimeError("AQ.Ab8RN6IC4VGSSCbbE5FyyV7tpvaF6yEG5ZlCBYztJ5RdKk-GkA")

client = genai.Client(api_key=API_KEY)


# Home Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "Khalil AI Assistant is running!"
    })


# Health Check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    })


# AI Chat Route
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}

        user_message = data.get("message", "")

        if not isinstance(user_message, str):
            return jsonify({
                "error": "Message must be text."
            }), 400

        user_message = user_message.strip()

        if not user_message:
            return jsonify({
                "error": "Please provide a message."
            }), 400

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message
        )

        return jsonify({
            "reply": response.text
        })

    except Exception:
        app.logger.exception("Chat request failed")

        return jsonify({
            "error": "AI request failed. Please try again."
        }), 500


# Render Server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
