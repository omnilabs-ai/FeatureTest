from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import requests
import asyncio
import json
import time
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class ChatRequest(BaseModel):
    messages: List[dict]
    
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI server"}


@app.post("/smartchat")
async def smartchat(request: ChatRequest):
    print(request, "\n\n")

    api_key = "test-sk1o83e" # temporary api key

    # Create a generator function to stream the response
    def response_generator():
        # Make the request to the omnirouter with stream=True to get a streaming response
        response = requests.post(
            "https://omnirouter.onrender.com/v1/router/smart_select/stream",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"messages": request.messages},  # Use the actual messages from the request
        )
        
        # Check if the request was successful
        if response.status_code != 200:
            yield f"data: {{'error': 'Received status code {response.status_code}'}}\n\n"
            return
            
        # Stream the response chunks
        for line in response.iter_lines():
            if line:
                print("Sending content:", line, "at time:", time.time())
                # Forward the SSE data as is
                yield f"{line.decode('utf-8')}\n"
            
        # Send the [DONE] message
        yield "data: [DONE]\n\n"

    # Return a streaming response
    return StreamingResponse(
        response_generator(),
        media_type="text/event-stream"
    )


@app.post("/smartchat_mock")
def smartchat_mock(request: ChatRequest):
    print("Mock request received:", request, "\n\n")

    # Create a generator function to stream mock responses
    def simple_mock_generator():
        # Simple response text broken into words
        response_text = "This is a simple mock response that streams word by word with a small delay between each word to simulate real-time generation."
        words = response_text.split()
        
        for word in words:
            # Create a simple response format
            response = {"content": word + " "}
            print("Sending word:", word, "at time:", time.time())
            # Send the word
            yield f"data: {json.dumps(response)}\n\n"
            
            # Small delay between words
            time.sleep(0.3)
            
        # Send the [DONE] message
        yield "data: [DONE]\n\n"

    # Return a streaming response
    return StreamingResponse(
        simple_mock_generator(),
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
