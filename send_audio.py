import os
import urllib.request
import uuid

print("--- SCRIPT STARTED ---")

URL = "http://localhost:5678/webhook-test/fd8cf684-9a5d-4a41-8595-7cf507d5ef76"
FILE = "sample_voice.mp3"

if not os.path.exists(FILE):
    print("Error: sample_voice.mp3 not found!")
else:
    print("Sending audio to n8n...")
    try:
        boundary = "----PythonBoundary" + uuid.uuid4().hex
        with open(FILE, "rb") as f:
            audio_data = f.read()

        body = (
            f"--{boundary}\r\n"
            'Content-Disposition: form-data; name="file"; filename="sample_voice.mp3"\r\n'
            "Content-Type: audio/mpeg\r\n\r\n"
        ).encode("utf-8") + audio_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

        req = urllib.request.Request(
            URL,
            data=body,
            headers={
                "Content-Type": f"multipart/form-data; boundary={boundary}"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=60) as response:
            print("Status:", response.status)
            print("Response:", response.read().decode("utf-8", errors="replace"))

    except Exception as e:
        print("Error:", e)
