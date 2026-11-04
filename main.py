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
