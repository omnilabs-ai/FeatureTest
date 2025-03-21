#!/usr/bin/env python3
import requests
import argparse
import json
from pprint import pprint


url = "https://omnirouter.onrender.com/v1/chat/completions"
api_key = "omni-h92zRKQFy6doJW7GEpGwBDhutLFJuXXZ"
    
# Set up headers with API key
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

body = {
    "model": "claude-3-5-sonnet",
    "messages": [
        {
            "role": "user",
            "content": "Hello, how are you?"
        }
    ]
}

response = requests.post(url, headers=headers, json=body)

print(response.json())
