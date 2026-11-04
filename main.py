import os
import requests
from openai import OpenAI

# Sahi tareeqa: Render par banaye gaye variable ka naam dein
client = OpenAI(api_key=os.environ.get("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"))

# n8n Webhook URL
URL = 'https://mop-upcountry-enigmatic.ngrok-free.dev'
FILE = 'sample_voice.mp3'

print('--- SCRIPT STARTED ---')

if not os.path.exists(FILE):
    print(f'Error: {FILE} not found in folder!')
else:
    print(f'Transcribing {FILE} using OpenAI Whisper...')
    try:
        # 1. Audio file ko OpenAI Whisper API ke zariye text mein convert karein
        with open(FILE, 'rb') as audio_file:
            transcript_response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        
        transcript_text = transcript_response.text
        print(f'✅ Transcript Generated: "{transcript_text}"')

        # 2. Ab yeh transcript JSON payload mein rakh kar n8n webhook ko POST karein
        print('Sending transcript to n8n webhook...')
        payload = {'transcript': transcript_text}
        r = requests.post(URL, json=payload)
        
        print('Status:', r.status_code)
        print('Response:', r.text)

    except Exception as e:
        print('❌ Error:', e)
