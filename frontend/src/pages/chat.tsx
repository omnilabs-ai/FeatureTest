import React, { useState } from 'react';
import axios from 'axios';

const Chat = () => {
    const [responseText, setResponseText] = useState('Response will appear here');
    const [isLoading, setIsLoading] = useState(false);
    const [metadata, setMetadata] = useState("");

    const handleSendMessage = async () => {
        try {
            setResponseText('');
            setMetadata("");
            const payload = {
                userid: 'user123',
                messages: [
                    { role: 'user', content: 'Build a python script that is a fastapi server that prints "Hello, World!" to the console.' }
                ],
                max_latency: 'BALANCED',
                max_cost: 'BALANCED',
                model_list: []
            };
            
            const response = await fetch('http://localhost:9000/smartchat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'text/event-stream'
                },
                body: JSON.stringify(payload)
            });
    
            if (!response.ok) {
                throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
            }
            
            if (!response.body) {
                throw new Error('Response body is null');
            }
    
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            
            // Keep track of previously processed events to avoid duplicates
            const processedEvents = new Set();
            
            while (true) {
                const { value, done } = await reader.read();
                
                if (done) break;
                
                const chunk = decoder.decode(value, { stream: true });
                const lines = chunk.split('\n');
                
                let currentEvent = null;
                
                for (const line of lines) {
                    if (line.startsWith('event:')) {
                        currentEvent = line.substring(6).trim();
                    } else if (line.startsWith('data:') && currentEvent) {
                        const data = JSON.parse(line.substring(5).trim());
                        // Create a unique key for this event+data combination
                        const eventKey = `${currentEvent}:${data}`;
                        
                        // Only log if we haven't seen this exact event+data before
                        if (!processedEvents.has(eventKey)) {
                            console.log(`[${new Date().toISOString()}] Event: ${currentEvent}, Data: ${data}`);
                            processedEvents.add(eventKey);
                        }
                        if (currentEvent === 'routing') {
                            setMetadata(data);
                            // await new Promise(resolve => setTimeout(resolve, 1000));
                        }
                        if (currentEvent === 'completion') {
                            setResponseText(prevText => prevText + data);
                        }
                    }
                }
            }
            
        } catch (error) {
            console.error('Streaming error:', error);
        }
    };
    
    
    

    return (
        <div>
            <h1>Chat Page (unprotected)</h1>
            <button 
                onClick={handleSendMessage} 
                disabled={isLoading}
            >
                {isLoading ? 'Loading...' : 'Send Message'}
            </button>
            <div id="response" style={{ 
                marginTop: '20px', 
                padding: '10px', 
                border: '1px solid #ccc', 
                borderRadius: '5px',
                minHeight: '100px',
                whiteSpace: 'pre-wrap'
            }}>
                <p>{responseText}</p>
            </div>
            {metadata && (
                <div style={{ marginTop: '20px' }}>
                    <h3>Metadata:</h3>
                    <pre>{JSON.stringify(metadata, null, 2)}</pre>
                </div>
            )}
        </div>
    );
};

export default Chat;

