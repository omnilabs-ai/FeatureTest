#!/usr/bin/env python3
import requests
import json
import sseclient
import time

print("Starting test_stream.py")

def test_stream():
    # url = "http://127.0.0.1:8000/v1/chat/completions/stream"
    url = "https://omnirouter.onrender.com/v1/chat/completions/stream"
    api_key = "omni-fnBjMyX738GAZMVIlyYhTXncoMqVkvAu"
    
    # Set up headers with API key
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream'  # Important for SSE streaming
    }

    body = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": "Hello, how are you?"
            }
        ],
    }
    # Make the request with stream=True to get the response as it comes
    response = requests.post(url, headers=headers, json=body, stream=True)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        try:
            error_data = response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except json.JSONDecodeError:
            print(f"Error response: {response.text}")
        return
    
    # Create SSE client from the response
    client = sseclient.SSEClient(response)

    start_time = time.time()
    for event in client.events():
        elapsed_time = time.time() - start_time
        print(f"{elapsed_time:.2f}s [{event.event}]: {event.data}")

def test_smart_stream():
    # url = "https://omnirouter.onrender.com/v1/smartRouterStream"
    url = "http://127.0.0.1:8000/v1/smartRouterStream"
    api_key = "omni-fnBjMyX738GAZMVIlyYhTXncoMqVkvAu"

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream'  # Important for SSE streaming
    }

    messages = [
        {"role": "user", "content": "Hello, how are you?"}
    ]
    max_latency = "balanced"
    max_cost = "balanced"
    model_list = []

    response = requests.post(url, headers=headers, json={"messages": messages, "max_latency": max_latency, "max_cost": max_cost, "model_list": model_list})
    
    client = sseclient.SSEClient(response)  # Parse SSE automatically

    start_time = time.time()
    for event in client.events():
        elapsed_time = time.time() - start_time
        json_data = json.loads(event.data)
        print(f"{elapsed_time:.2f}s [{event.event}]: {json_data}")
        if event.event == "return":
            print(json_data["model"])


if __name__ == "__main__":
    test_smart_stream()
    # test_stream()
