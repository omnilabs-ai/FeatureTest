import requests
import json
import time

# response = requests.post(
#     "http://localhost:9000/smartchat_mock",
#     headers={"Authorization": f"Bearer test-sk1o83e"},
#     json={"messages": [{"role": "user", "content": "Say 'Hello, test!' in a friendly way."}]}
# )

# print("Starting to receive chunks...")
# for line in response.iter_lines():
#     line = line.decode() if isinstance(line, bytes) else line
#     if line.startswith('data: '):
#         data = line[6:]  # Remove 'data: ' prefix
#         if data == '[DONE]':
#             break

#         chunk_data = json.loads(data)
#         chunk_content = chunk_data.get('content', '')
#         print(f"Received chunk at {time.strftime('%H:%M:%S')}: {chunk_content}")
#         # Flush stdout to ensure immediate printing
#         import sys
#         sys.stdout.flush()

# url = "http://localhost:9000/smartchat"
# # url = "https://omnirouter.onrender.com/v1/smartchat"

# response = requests.post(
#     url,
#     headers={"Authorization": f"Bearer test-sk1o83e"},
#     json={"messages": [{"role": "user", "content": "Say 'Hello, test!' in a friendly way."}]}
# )

# print("Starting to receive chunks...")
# for line in response.iter_lines():
#     line = line.decode() if isinstance(line, bytes) else line
#     print(line)
#     if line.startswith('data: '):
#         data = line[6:]  # Remove 'data: ' prefix
#         if data == '[DONE]':
#             break

#         chunk_data = json.loads(data)
#         chunk_content = chunk_data.get('content', '')
#         print(f"Received chunk at {time.strftime('%H:%M:%S')}: {chunk_content}")
#         # Flush stdout to ensure immediate printing
#         import sys
#         sys.stdout.flush()