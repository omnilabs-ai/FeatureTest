import React, { useState, useEffect } from "react";

const ProductDisplay = () => (
  <section>
    <div className="product">
      <img
        src="https://i.imgur.com/EHyR2nP.png"
        alt="The cover of Stubborn Attachments"
      />
      <div className="description">
        <h3>Stubborn Attachments</h3>
        <h5>$20.00</h5>
      </div>
    </div>
    <button 
      onClick={async () => {
        try {
          const response = await fetch('http://localhost:4242/create-checkout-session', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            }
          });
          const { url } = await response.json();
          console.log(url);
          window.location.href = url;
        } catch (error) {
          console.error('Error:', error);
        }
      }}
      className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-md"
    >
      Checkout
    </button>
  </section>
);

const Message = ({ message }: { message: string }) => (
  <section>
    <p>{message}</p>
  </section>
);

export default function Payments() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    // Check to see if this is a redirect back from Checkout
    const query = new URLSearchParams(window.location.search);

    if (query.get("success")) {
      setMessage("Order placed! You will receive an email confirmation.");
    }

    if (query.get("canceled")) {
      setMessage(
        "Order canceled -- continue to shop around and checkout when you're ready."
      );
    }
  }, []);

  return message ? (
    <Message message={message} />
  ) : (
    <ProductDisplay />
  );
}