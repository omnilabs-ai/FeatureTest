#!/usr/bin/env python3
import requests
import argparse
import json
from pprint import pprint


url = "http://127.0.0.1:8000/v1/chat/completions"
api_key = "omni-h92zRKQFy6doJW7GEpGwBDhutLFJuXXZ"
    
# Set up headers with API key
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

body = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "user",
            "content": "Hello, how are you?"
        }
    ]
}

response = requests.post(url, headers=headers, json=body)

if response.status_code != 200:
    print(f"Error: Received status code {response.status_code}")
    try:
        error_data = response.json()
        print(f"Error details: {json.dumps(error_data, indent=2)}")
    except json.JSONDecodeError:
        print(f"Error response: {response.text}")
else:
    print(response.json())
