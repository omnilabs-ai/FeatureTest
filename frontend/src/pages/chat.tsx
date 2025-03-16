import React, { useState } from 'react';

const Chat = () => {
    const [responseText, setResponseText] = useState('Response will appear here');
    const [isLoading, setIsLoading] = useState(false);

    const handleSendMessage = async () => {
        try {
            setIsLoading(true);
            setResponseText('');
            
            const response = await fetch("http://localhost:9000/smartchat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ 
                    messages: [{ role: "user", content: "Write me a page long poem about a cat" }] 
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Create a new ReadableStream from the response body
            const reader = response.body?.getReader();
            if (!reader) {
                throw new Error('Response body is not readable');
            }

            // Read the stream
            const decoder = new TextDecoder();
            let buffer = '';
            let done = false;
            
            while (!done) {
                const { value, done: doneReading } = await reader.read();
                done = doneReading;
                
                if (value) {
                    // Decode the chunk and add it to our buffer
                    buffer += decoder.decode(value, { stream: !done });
                    
                    // Process any complete messages in the buffer
                    const lines = buffer.split('\n');
                    buffer = lines.pop() || ''; // Keep the last incomplete line in the buffer
                    
                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            const data = line.slice(6); // Remove 'data: ' prefix
                            
                            if (data === '[DONE]') {
                                continue;
                            }
                            
                            try {
                                const parsed = JSON.parse(data);
                                if (parsed.content) {
                                    setResponseText(prev => prev + parsed.content);
                                }
                                if (parsed.error) {
                                    setResponseText(prev => prev + '\nError: ' + parsed.error);
                                }
                            } catch (e) {
                                console.warn('Failed to parse SSE data:', data);
                            }
                        }
                    }
                }
            }
        } catch (error: any) {
            console.error('Error:', error);
            setResponseText(`Error: ${error.message || 'Unknown error occurred'}`);
        } finally {
            setIsLoading(false);
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
        </div>
    );
};

export default Chat;

