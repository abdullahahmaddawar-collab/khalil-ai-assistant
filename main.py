import os
import requests
from openai import OpenAI

# Apni OpenAI API key yahan enter karein (ya environment variable set karein)
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

# n8n Webhook URL
URL = 'http://localhost:5678/webhook-test/fd8cf684-9a5d-4a41-8595-7cf507d5ef76'
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