import asyncio
import aiohttp
import time
import json
from datetime import datetime

BASE_URL = "http://localhost:9100"

# Track the start time of the test
start_time = None
# Track received events for each client
client_events = {}

async def connect_and_stream(client_id, endpoint="/streamasync", expected_messages=10):
    """Connect to the streaming endpoint and collect messages"""
    global client_events
    
    client_events[client_id] = []
    url = f"{BASE_URL}{endpoint}"
    
    print(f"Client {client_id}: Connecting to {url}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"Client {client_id}: Error - Received status {response.status}")
                    return False
                
                # Process the streaming response
                print(f"Client {client_id}: Connected, receiving stream...")
                
                # Track when this client started receiving
                client_start_time = time.time() - start_time
                client_events[client_id].append({
                    "event": "connected", 
                    "time_offset": client_start_time
                })
                
                # Read the SSE stream
                async for line in response.content:
                    line = line.decode('utf-8').strip()
                    
                    # SSE format - data: {...}
                    if line.startswith('data: '):
                        data_str = line[6:]  # Remove 'data: ' prefix
                        
                        # Check if it's the completion message
                        if 'complete' in line:
                            client_events[client_id].append({
                                "event": "complete",
                                "time_offset": time.time() - start_time
                            })
                            print(f"Client {client_id}: Stream complete")
                            break
                            
                        # Otherwise it's a data message
                        try:
                            data = json.loads(data_str)
                            client_events[client_id].append({
                                "data": data,
                                "time_offset": time.time() - start_time
                            })
                            print(f"Client {client_id}: Received message {data.get('id', 'unknown')}")
                            
                            # If we've received all expected messages, we can stop
                            if len([e for e in client_events[client_id] if 'data' in e]) >= expected_messages:
                                print(f"Client {client_id}: Received all expected messages")
                                break
                                
                        except json.JSONDecodeError:
                            print(f"Client {client_id}: Failed to parse JSON: {data_str}")
                    
                print(f"Client {client_id}: Disconnected")
                return True
                
    except Exception as e:
        print(f"Client {client_id}: Exception occurred: {str(e)}")
        return False

async def run_concurrent_test(num_clients=5, endpoint="/streamasync"):
    """Run a test with multiple concurrent clients"""
    global start_time
    
    print(f"Starting concurrent test with {num_clients} clients on {endpoint}")
    start_time = time.time()
    
    # Create tasks for all clients
    tasks = [connect_and_stream(f"client-{i}", endpoint) for i in range(num_clients)]
    
    # Run all tasks concurrently
    results = await asyncio.gather(*tasks)
    
    # Check if all clients succeeded
    all_succeeded = all(results)
    
    # Analyze the results
    print("\n--- Test Results ---")
    if all_succeeded:
        print(f"✅ All {num_clients} clients completed successfully")
    else:
        print(f"❌ {results.count(False)}/{num_clients} clients failed")
    
    # Analyze timing
    analyze_timing()
    
    return all_succeeded

def analyze_timing():
    """Analyze the timing of events to check concurrency"""
    print("\n--- Timing Analysis ---")
    
    # Check connection times
    connection_times = {client: next((e["time_offset"] for e in events if e["event"] == "connected"), None)
                       for client, events in client_events.items()}
    
    print(f"Connection times: {connection_times}")
    
    # Calculate how many clients were receiving data simultaneously
    # Get all message receipt times for each client
    all_message_times = []
    for client, events in client_events.items():
        for event in events:
            if 'data' in event:
                all_message_times.append((event["time_offset"], client, event["data"].get("id", "unknown")))
    
    # Sort by timestamp
    all_message_times.sort()
    
    # Output timeline
    print("\nMessage Timeline:")
    for time_offset, client, msg_id in all_message_times:
        print(f"{time_offset:.2f}s: {client} received message {msg_id}")
    
    # Check if the server is truly handling requests concurrently
    # In a concurrent server, we should see interleaved messages from different clients
    # rather than one client receiving all messages before the next one starts
    
    # Group events by second
    events_by_second = {}
    for time_offset, client, msg_id in all_message_times:
        second = int(time_offset)
        if second not in events_by_second:
            events_by_second[second] = []
        events_by_second[second].append((client, msg_id))
    
    # Check for time windows with multiple clients receiving data
    concurrent_seconds = sum(1 for second, events in events_by_second.items() 
                           if len(set(client for client, _ in events)) > 1)
    
    print(f"\nTime windows with concurrent message delivery: {concurrent_seconds} seconds")
    
    if concurrent_seconds > 0:
        print("✅ The server appears to be handling requests concurrently")
    else:
        print("❌ The server may not be truly concurrent - no overlapping message delivery detected")

if __name__ == "__main__":
    # Test both endpoints
    for endpoint in ["/stream", "/streamasync"]:
        print(f"\n{'='*50}")
        print(f"Testing endpoint: {endpoint}")
        print(f"{'='*50}\n")
        
        # Reset the client events for each test
        client_events = {}
        
        # Run the test
        asyncio.run(run_concurrent_test(num_clients=3, endpoint=endpoint))
        
        print(f"\n{'='*50}")
        print(f"Test complete for {endpoint}")
        print(f"{'='*50}\n")
