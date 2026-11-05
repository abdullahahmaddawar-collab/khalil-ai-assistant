import os
import time
import requests

# Deepgram API Key ko environment variable se load karein
DEEPGRAM_API_KEY = os.environ.get("abf41518e397a6d8dd8da41e1df068b965eeb24f")

URL = 'https://mop-upcountry-enigmatic.ngrok-free.dev'
FILE = 'sample_voice.mp3'

print('--- SCRIPT STARTED (USING DEEPGRAM NOVA-2 API) ---')

if not os.path.exists(FILE):
    print(f'Error: {FILE} not found in folder!')
else:
    print(f'Processing {FILE} using Deepgram Nova-2...')
    
    max_retries = 3
    success = False
    
    for attempt in range(max_retries):
        try:
            # Deepgram API Endpoint with Nova-2 model
            deepgram_url = "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true"
            
            headers = {
                "Authorization": f"Token {DEEPGRAM_API_KEY}",
                "Content-Type": "audio/mp3"
            }
            
            with open(FILE, "rb") as f:
                audio_data = f.read()
                
            response = requests.post(deepgram_url, headers=headers, data=audio_data)
            
            if response.status_code == 200:
                result = response.json()
                # Deepgram JSON response se transcript extract karna
                transcript_text = result["results"]["channels"][0]["alternatives"][0]["transcript"].strip()
                print(f'✅ Transcript Generated: "{transcript_text}"')

                print('Sending transcript to n8n webhook...')
                payload = {'transcript': transcript_text}
                r = requests.post(URL, json=payload)
                
                print('Status:', r.status_code)
                print('Response:', r.text)
                success = True
                break
            else:
                raise Exception(f"Deepgram API Error: {response.status_code} - {response.text}")

        except Exception as e:
            print(f'⚠️ Attempt {attempt + 1} failed with error: {e}')
            if attempt < max_retries - 1:
                print('Retrying in 5 seconds...')
                time.sleep(5)
            else:
                print('❌ All retry attempts failed.')
