import os
from flask import Flask, request, jsonify
from google import genai

print("DEBUG - Available Env Keys:", list(os.environ.keys()))

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable is missing")
