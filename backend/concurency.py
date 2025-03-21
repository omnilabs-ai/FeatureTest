from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio
import json
import time
from datetime import datetime

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Fake Streaming API"}

@app.get("/stream")
async def stream_data():
    """
    Endpoint that streams dummy data using SSE with 1-second delay
    """
    def generate():
        # Stream 10 messages as example
        for i in range(1, 11):
            # Prepare dummy data
            data = {
                "id": i,
                "message": f"This is dummy message #{i}",
                "timestamp": datetime.now().isoformat(),
                "value": i * 10
            }
            
            # Format as SSE data
            yield f"data: {json.dumps(data)}\n\n"
            
            # Wait 1 second before the next message
            time.sleep(1)
        
        # Send completion event
        yield "event: complete\ndata: {\"status\": \"finished\"}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )

@app.get("/streamasync")
async def stream_async():
    """
    Endpoint that streams dummy data asynchronously using SSE with 1-second delay
    """
    async def generate_async():
        # Stream 10 messages as example
        for i in range(1, 11):
            # Prepare dummy data
            data = {
                "id": i,
                "message": f"This is async dummy message #{i}",
                "timestamp": datetime.now().isoformat(),
                "value": i * 10
            }
            
            # Format as SSE data
            yield f"data: {json.dumps(data)}\n\n"
            
            # Wait 1 second before the next message
            await asyncio.sleep(1)
        
        # Send completion event
        yield "event: complete\ndata: {\"status\": \"finished\"}\n\n"

    return StreamingResponse(
        generate_async(),
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("concurency:app", host="0.0.0.0", port=9100, reload=True)
