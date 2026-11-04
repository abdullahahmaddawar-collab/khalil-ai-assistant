from flask import Flask, render_template_string, request, jsonify
import json
import urllib.request
import urllib.error
import uuid
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS so Odoo (HTTPS) can communicate with the local proxy (HTTP)
CORS(app)

# Purana URL (Test mode - ise hata dein)
# N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/fd8cf684-9a5d-4a41-8595-7cf507d5ef76"

# Naya URL (Production mode - yeh lagayein)
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/fd8cf684-9a5d-4a41-8595-7cf507d5ef76"

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Khalil AI Voice Assistant</title>

<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #212121;
    color: white;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

header {
    padding: 20px;
    font-size: 22px;
    border-bottom: 1px solid #444;
}

main {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
    gap: 25px;
}

#status {
    color: #bbb;
    text-align: center;
}

#mic {
    width: 90px;
    height: 90px;
    border: 0;
    border-radius: 50%;
    background: #303030;
    color: white;
    font-size: 38px;
    cursor: pointer;
}

#mic:hover { background: #454545; }

#mic:disabled {
    opacity: 0.5;
    cursor: wait;
}

#result {
    width: 100%;
    max-width: 650px;
    padding: 20px;
    border: 1px solid #444;
    border-radius: 12px;
    background: #292929;
    line-height: 1.7;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

footer {
    padding: 18px;
    text-align: center;
    color: #999;
    font-size: 13px;
}
</style>
</head>

<body>
<header>✦ Khalil AI</header>

<main>
    <h2>How can I help you?</h2>
    <div id="status">Press the microphone to start recording</div>
    <button id="mic" title="Start or stop recording">🎙️</button>
    <div id="result">Your voice command will appear here.</div>
</main>

<footer>AI Voice Assistant · Local Demo</footer>

<script>
const statusText = document.getElementById("status");
const result = document.getElementById("result");
const mic = document.getElementById("mic");

let recorder = null;
let audioChunks = [];
let recording = false;
let stream = null;

mic.onclick = async () => {
    if (recording) {
        recording = false;
        mic.textContent = "🎙️";
        mic.disabled = true;
        statusText.textContent = "Preparing audio...";
        recorder.stop();
        return;
    }

    try {
        if (!navigator.mediaDevices ||
            !navigator.mediaDevices.getUserMedia ||
            !window.MediaRecorder) {
            throw new Error(
                "Audio recording is not supported in this browser."
            );
        }

        stream = await navigator.mediaDevices.getUserMedia({
            audio: true
        });

        audioChunks = [];

        let mimeType = "";

        if (MediaRecorder.isTypeSupported("audio/webm;codecs=opus")) {
            mimeType = "audio/webm;codecs=opus";
        } else if (MediaRecorder.isTypeSupported("audio/webm")) {
            mimeType = "audio/webm";
        }

        recorder = mimeType
            ? new MediaRecorder(stream, { mimeType })
            : new MediaRecorder(stream);

        recorder.ondataavailable = (event) => {
            if (event.data && event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        recorder.onerror = (event) => {
            statusText.textContent = "Recording error occurred.";
            mic.disabled = false;
        };

        recorder.onstop = async () => {
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
                stream = null;
            }

            const audioBlob = new Blob(audioChunks, {
                type: recorder.mimeType || "audio/webm"
            });

            if (!audioBlob.size) {
                statusText.textContent =
                    "No audio recorded. Please try again.";
                mic.disabled = false;
                return;
            }

            result.textContent =
                "Recorded audio: " +
                Math.round(audioBlob.size / 1024) +
                " KB";

            statusText.textContent = "Sending audio to n8n...";

            const formData = new FormData();
            formData.append("file", audioBlob, "voice-command.webm");

            try {
                const response = await fetch("/process-voice", {
                    method: "POST",
                    body: formData
                });

                const responseText = await response.text();
                let data;

                try {
                    data = JSON.parse(responseText);
                } catch (_) {
                    throw new Error(
                        "Invalid server response: " + responseText
                    );
                }

                if (!response.ok) {
                    throw new Error(
                        data.details || data.error || "Request failed"
                    );
                }

                let answer = data.n8n_response;

                if (typeof answer === "string") {
                    try {
                        answer = JSON.parse(answer);
                    } catch (_) {}
                }

                if (Array.isArray(answer) && answer.length > 0) {
                    answer = answer[0];
                }

                result.textContent =
                    "Audio uploaded: " + data.filename +
                    "\nAudio size: " + data.audio_bytes + " bytes" +
                    "\n\nn8n response:\n" +
                    (typeof answer === "string"
                        ? answer
                        : JSON.stringify(answer, null, 2));

                statusText.textContent = "Response received.";

            } catch (error) {
                statusText.textContent = "Error: " + error.message;
                result.textContent =
                    "Could not process audio.\n\n" + error.message;
            } finally {
                mic.disabled = false;
            }
        };

        recorder.start();
        recording = true;
        mic.textContent = "⏹️";
        statusText.textContent = "Recording... Press again to stop.";
        result.textContent = "Listening to your voice command...";

    } catch (error) {
        statusText.textContent = "Microphone error: " + error.message;

        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }

        mic.disabled = false;
        recording = false;
        mic.textContent = "🎙️";
    }
};
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/process-voice", methods=["POST", "OPTIONS"])
def process_voice():
    # Handle CORS Preflight request
    if request.method == "OPTIONS":
        return '', 200

    audio = request.files.get("file")

    if not audio or not audio.filename:
        return jsonify({
            "error": "Audio file missing. Expected field 'file'."
        }), 400

    audio_bytes = audio.read()

    if not audio_bytes:
        return jsonify({
            "error": "Audio file is empty."
        }), 400

    boundary = "----KhalilBoundary" + uuid.uuid4().hex
    filename = audio.filename.replace('"', "")
    content_type = audio.mimetype or "audio/webm"

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode("utf-8")

    body += audio_bytes
    body += f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(
        N8N_WEBHOOK_URL,
        data=body,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body))
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            response_body = response.read().decode(
                "utf-8", errors="replace"
            )

            try:
                n8n_response = json.loads(response_body)
            except json.JSONDecodeError:
                n8n_response = response_body

            return jsonify({
                "sent": True,
                "filename": filename,
                "audio_bytes": len(audio_bytes),
                "n8n_response": n8n_response
            })

    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")

        return jsonify({
            "error": "n8n returned HTTP " + str(error.code),
            "details": details
        }), 502

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 502


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=True
    )