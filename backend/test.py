import requests
import json
from datetime import datetime

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
# url = "http://localhost:8000/v1/chat/completions/stream"
url = "https://omnirouter.onrender.com/v1/chat/completions/stream"

start_time = datetime.now()
print(f"[+0.000000s] Starting request...")

response = requests.post(
    url,
    headers={"Authorization": f"Bearer test-sk1o83e"},
    json={
        "messages": [{"role": "user", "content": "Say 'Hello, test!' in a friendly way."}],
        "model": "gpt-4o-mini"
    }
)

print("[+{:.6f}s] Starting to receive chunks...".format((datetime.now() - start_time).total_seconds()))
for line in response.iter_lines():
    line = line.decode() if isinstance(line, bytes) else line
    if line.startswith('data: '):
        data = line[6:]  # Remove 'data: ' prefix
        if data == '[DONE]':
            break

        chunk_data = json.loads(data)
        chunk_content = chunk_data.get('content', '')
        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"[+{elapsed:.6f}s] Chunk content: {chunk_content}")
        # Flush stdout to ensure immediate printing
        import sys
        sys.stdout.flush()

total_time = (datetime.now() - start_time).total_seconds()
print(f"\nTotal time: {total_time:.6f}s")