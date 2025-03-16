import React, { useState } from "react";

export default function ApiKeyGenerator() {
  const [apiKey, setApiKey] = useState<string | null>(null);

  const generateApiKey = async () => {
    // Generate a random string
    const randomString = crypto.getRandomValues(new Uint8Array(32))
      .reduce((acc, byte) => acc + byte.toString(16).padStart(2, "0"), "");

    // Hash it using SHA-256 for better uniqueness
    const encoder = new TextEncoder();
    const data = encoder.encode(randomString);
    const hashBuffer = await crypto.subtle.digest("SHA-256", data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, "0")).join("");

    // Trim to 32 characters for API key length
    setApiKey("omni-" + hashHex.substring(0, 32));
  };

  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <h2>API Key Generator</h2>
      <button onClick={generateApiKey} style={{ padding: "10px", cursor: "pointer" }}>
        Generate API Key
      </button>
      {apiKey && (
        <div style={{ marginTop: "20px" }}>
          <strong>Your API Key:</strong>
          <p style={{ background: "#f4f4f4", padding: "10px", borderRadius: "5px", wordBreak: "break-all" }}>
            {apiKey}
          </p>
        </div>
      )}
    </div>
  );
}
