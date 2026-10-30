import os
import requests

# Production Tunnel URL (apna actual active tunnel link yahan rakhein):
URL = 'https://aapka-tunnel-url.lhr.life/webhook/fd8cf684-9a5d-4a41-8595-7cf507d5ef76'

FILE = 'sample_voice.mp3'
print('--- SCRIPT STARTED ---')

if not os.path.exists(FILE):
    print(f'Error: {FILE} not found in folder!')
else:
    print(f'Sending {FILE}...')
    try:
        with open(FILE, 'rb') as f:
            headers = {'Bypass-Tunnel-Reminder': 'true'}
            r = requests.post(URL, files={'file': (FILE, f, 'audio/mpeg')}, headers=headers)
            print('Status:', r.status_code)
            print('Response:', r.text)
    except Exception as e:
        print('Error:', e)