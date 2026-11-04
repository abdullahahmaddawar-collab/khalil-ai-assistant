import os
import requests
<<<<<<< HEAD
from openai import OpenAI

# Apni OpenAI API key yahan enter karein (ya environment variable set karein)
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

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
=======

# Agar aap production URL use kar rahe hain (recommended):
URL = 'https://mop-upcountry-enigmatic.ngrok-free.dev'

# Ya agar test URL hi rakhna hai toh n8n wala exact path match karein:
# URL = 'http://localhost:5678/webhook-test/voice-command'

FILE = 'sample_voice.mp3'
print('--- SCRIPT STARTED ---')

if not os.path.exists(FILE):
  print(f'Error: {FILE} not found in folder!')
else:
  print(f'Sending {FILE}...')
  try:
    with open(FILE, 'rb') as f:
      r = requests.post(URL, files={'file': (FILE, f, 'audio/mpeg')})
      print('Status:', r.status_code)
      print('Response:', r.text)
  except Exception as e:
    print('Error:', e)
>>>>>>> 960cdd7
