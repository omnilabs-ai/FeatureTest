const handleSendMessage = async () => {
    try {
        const payload = {
            userid: 'user123',
            messages: [
                { role: 'user', content: 'What is the capital of France?' }
            ],
            max_latency: 'BALANCED',
            max_cost: 'BALANCED',
            model_list: []
        };

        console.log('Making request to server using fetch directly...');
        
        // Use fetch directly for better stream control
        const response = await fetch('http://localhost:9000/smartchat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'text/event-stream'
            },
            body: JSON.stringify(payload)
        });

        console.log('Server responded with status:', response.status);
        
        if (!response.ok) {
            throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
        }
        
        if (!response.body) {
            console.error('Response body is null');
            return;
        }

        // Get a reader from the response body stream
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        console.log('Starting to read stream...');
        
        while (true) {
            const { value, done } = await reader.read();
            
            if (done) {
                console.log('Stream is done');
                break;
            }
            
            // Decode the chunk
            const chunk = decoder.decode(value, { stream: true });
            
            // Process each line individually
            const lines = chunk.split('\n');
            
            let currentEvent = null;
            let currentData = null;
            
            for (const line of lines) {
                if (line.startsWith('event:')) {
                    // If we already have an event and data, log them before starting a new event
                    if (currentEvent && currentData) {
                        console.log(`Event: ${currentEvent}, Data: ${currentData}`);
                    }
                    
                    currentEvent = line.substring(6).trim();
                    currentData = null;
                } else if (line.startsWith('data:')) {
                    currentData = line.substring(5).trim();
                    
                    // If we have both event and data, log them immediately
                    if (currentEvent) {
                        console.log(`Event: ${currentEvent}, Data: ${currentData}`);
                    }
                }
            }
        }
        
        console.log('Stream processing complete');
        
    } catch (error) {
        console.error('Streaming error:', error);
    }
};