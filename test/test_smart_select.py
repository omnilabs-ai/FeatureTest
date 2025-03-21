base_url = "http://127.0.0.1:9000/smartchat"

import requests
import json
import sseclient
def test_simple_request():
    # Test data
    request_data = {
        "userid": "IiRH9ajwJ0QEVcv1tExKD1c6rG52",  # You'll need a valid user ID from your Firestore
        "messages": [
            {
                "role": "user",
                "content": "Hello, how are you?"
            }
        ],
        "max_latency": "BALANCED",
        "max_cost": "BALANCED",
        "model_list": []
    }

    # Make the request
    response = requests.post(
        base_url,
        json=request_data,
        headers={
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }
    )

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print(response.text)
        exit()

    client = sseclient.SSEClient(response)

    for event in client.events():
        print(event.event, event.data)

    # # Since this is a streaming response, we need to read the events
    # for line in response.iter_lines():
    #     if line:
    #         # Decode the line and remove "data: " prefix if it exists
    #         decoded_line = line.decode('utf-8')
    #         if decoded_line.startswith('data: '):
    #             data = decoded_line[6:]  # Remove "data: " prefix
    #             try:
    #                 event_data = json.loads(data)
    #                 print(f"Received event: {event_data}")
    #             except json.JSONDecodeError:
    #                 print(f"Could not parse line as JSON: {data}")


if __name__ == "__main__":
    test_simple_request()

