import whisper

print('Loading local Whisper model...')
model = whisper.load_model('base')

print('Transcribing audio...')
result = model.transcribe('sample_voice.mp3')

print('\n--- TRANSCRIBED TEXT ---')
print(result['text'])
