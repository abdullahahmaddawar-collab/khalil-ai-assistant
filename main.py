
import os
import time
import requests
from google import genai

# Gemini API key from Render Environment
client = genai.Client(
    api_key=os.environ.get("AQ.Ab8RN6J4jY-R5wm7_jgJNAJwtFKZWmbQHbUWpJ81z3kTdTV05g")
)

# n8n production webhook URL
URL = 'https://mop-upcountry-enigmatic.ngrok-free.dev/webhook/fd8cf684-9a5d-4a41-8595-7cf507d5ef76'

FILE = "sample_voice.mp3"

print("--- KHALIL AI STARTED ---")

if not URL:
    raise ValueError("N8N_WEBHOOK_URL is missing!")

if not os.path.exists(FILE):
    print(f"Error: {FILE} not found!")
else:
    print(f"Processing {FILE} using Gemini...")

    for attempt in range(3):
        try:
            audio_file = client.files.upload(file=FILE)

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    audio_file,
                    "Provide an accurate, clean text transcription."
                ]
            )

            transcript_text = response.text.strip()

            print("Transcript:", transcript_text)

            payload = {
                "transcript": transcript_text
            }

            print("Sending transcript to n8n...")

            r = requests.post(
                URL,
                json=payload,
                timeout=60
            )

            r.raise_for_status()

            print("SUCCESS:", r.status_code)
            print("n8n Response:", r.text)
            break

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt < 2:
                time.sleep(5)
            else:
                print("All attempts failed!")
