from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List
import requests
import json
import time
import sseclient
from sse_starlette.sse import EventSourceResponse

app = FastAPI()

# Configure CORS middleware properly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow both localhost and 127.0.0.1
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Explicitly list allowed methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"],  # Expose all headers to the browser
)
    
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI server"}

class ChatMessage(BaseModel):
    role: str
    content: str

class SmartRouterRequest(BaseModel):
    userid: str = Field(..., description="User ID")
    messages: List[ChatMessage] = Field(..., description="List of messages in the conversation")
    max_latency: str = Field(..., description="Maximum latency preference (LIGHTNING, FAST, BALANCED, PERFORMANCE)")
    max_cost: str = Field(..., description="Maximum cost preference (CHEAP, BALANCED, PREMIUM, PERFORMANCE)")
    model_list: list = Field(..., description="List of models to consider (optional)")

base_url = "http://omnirouter.onrender.com/v1"

@app.post("/smartchat")
async def stream_completion(request: SmartRouterRequest):
    print(request)
    # Convert messages to dict format
    messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
    api_key = "omni-fnBjMyX738GAZMVIlyYhTXncoMqVkvAu"

    async def response_generator():
        response = requests.post(
            f"{base_url}/smartRouterStream", 
            headers={"Authorization": f"Bearer {api_key}"}, 
            json={
                "messages": messages,
                "max_latency": request.max_latency,
                "max_cost": request.max_cost,
                "model_list": request.model_list
            }
        )

        if response.status_code != 200:
            yield {
                "event": "error",
                "data": json.dumps({"error": f"Request failed with status {response.status_code}: {response.text}"})
            }
            return

        client = sseclient.SSEClient(response)
        
        selected_model = None
        headers = {"Authorization": f"Bearer {api_key}"}

        exclusion_events = ["metadata", "usage"]
        for event in client.events():
            event_data = json.loads(event.data)

            if event.event == "return":
                selected_model = event_data["model"]
            else:
                yield {
                    "event": "routing",
                    "data": json.dumps(event_data["message"])
                }

        print(selected_model)

        response = requests.post(
            f"{base_url}/chat/completions/stream", 
            headers=headers, 
            json={
                "messages": messages,
                "model": selected_model
            }
        )
        if response.status_code != 200:
            yield {
                "event": "error",
                "data": json.dumps({"error": f"Request failed with status {response.status_code}: {response.text}"})
            }
            return

        client = sseclient.SSEClient(response)

        for event in client.events():
            if event.event in exclusion_events:
                continue
            event_data = json.loads(event.data)
            yield {
                "event": "completion",
                "data": json.dumps(event_data["content"])
            }

    return EventSourceResponse(response_generator())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
