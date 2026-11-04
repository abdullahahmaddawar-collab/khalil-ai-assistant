import os
import requests
from google import genai

# Environment variable se Gemini API key load hogi
client = genai.Client(api_key=os.environ.get("AQ.Ab8RN6IqMa82wbTetG14sZMBmekRkAStsFEJy-VyD0D7RtAvsA"))

URL = 'https://mop-upcountry-enigmatic.ngrok-free.dev'
FILE = 'sample_voice.mp3'

print('--- SCRIPT STARTED (USING GOOGLE GEMINI API) ---')

if not os.path.exists(FILE):
    print(f'Error: {FILE} not found in folder!')
else:
    print(f'Processing {FILE} using Gemini...')
    try:
        # 1. Audio file ko upload karke Gemini ke zariye transcribe/process karein
        audio_file = client.files.upload(file=FILE)
        
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=[
                audio_file,
                "Please provide an accurate, clean text transcription of this audio file, with no extra commentary."
            ]
        )
        
        transcript_text = response.text.strip()
        print(f'✅ Transcript Generated: "{transcript_text}"')

        # 2. Transcript ko n8n webhook par POST karein
        print('Sending transcript to n8n webhook...')
        payload = {'transcript': transcript_text}
        r = requests.post(URL, json=payload)
        
        print('Status:', r.status_code)
        print('Response:', r.text)

    except Exception as e:
        print('❌ Error:', e)
