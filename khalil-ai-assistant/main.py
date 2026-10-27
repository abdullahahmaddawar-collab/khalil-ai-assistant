import os
import requests

# Agar aap production URL use kar rahe hain (recommended):
URL = 'http://localhost:5678/webhook/fd8cf684-9a5d-4a41-8595-7cf507d5ef76'

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