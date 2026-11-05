import os
import time
import requests
from google import genai

# Render environment variable se GEMINI_API_KEY read karna
client = genai.Client(api_key=os.environ.get("AQ.Ab8RN6LAEbx7G4dGLwxGLOHmEZKbEEsXyjkGSlBITjTuD7VM4w"))

# Yahan ngrok domain ke sath n8n ka poora production webhook path dena zaroori hai
URL = 'https://mop-upcountry-enigmatic.ngrok-free.dev/webhook/fd8cf684-9a5d-4a41-8595-7cf507d5ef76'
FILE = 'sample_voice.mp3'

print('--- SCRIPT STARTED (USING GOOGLE GEMINI API) ---')

if not os.path.exists(FILE):
    print(f'Error: {FILE} not found in folder!')
else:
    print(f'Processing {FILE} using Gemini...')
    
    max_retries = 3
    success = False
    
    for attempt in range(max_retries):
        try:
            # Audio file upload to Gemini
            audio_file = client.files.upload(file=FILE)
            
            # Text transcription generation
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    audio_file,
                    "Please provide an accurate, clean text transcription of this audio file, with no extra commentary."
                ]
            )
            
            transcript_text = response.text.strip()
            print(f'✅ Transcript Generated: "{transcript_text}"')

            # Sending transcript to n8n webhook via ngrok tunnel
            print('Sending transcript to n8n webhook...')
            payload = {'transcript': transcript_text}
            r = requests.post(URL, json=payload)
            
            print('Status:', r.status_code)
            print('Response:', r.text)
            success = True
            break

        except Exception as e:
            print(f'⚠️ Attempt {attempt + 1} failed with error: {e}')
            if attempt < max_retries - 1:
                print('Retrying in 5 seconds...')
                time.sleep(5)
            else:
                print('❌ All retry attempts failed.')
