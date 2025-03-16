#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, jsonify, request, make_response, redirect
from flask_cors import CORS
import stripe

# CLI Testing

# stripe trigger payment_intent.succeeded --add payment_intent:metadata.customer_id=12345


# This is your test secret API key.
stripe.api_key = 'sk_test_51LHxqECMpfMOpId7h2wtZZPo3VtRPIT9q0Dk23ohum3MKsnhLHODIbRY6ZlII1IA1PaWvlmlRm79ONDLV98Q1muu00YS0lky3z'

app = Flask(__name__)
CORS(app)

YOUR_DOMAIN = 'http://localhost:3000'

endpoint_secret = 'whsec_fb879ee63c36abeecc424003b931c802ee2f69527d3cd14febc70186617841c2'

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)

        print(session['metadata'])
        # user_id = session['metadata']['user_id']
        # Here you can handle the successful payment
        # e.g., update your database, activate features for the user, etc.
        # print(f"Payment succeeded for user: {user_id}")
    elif event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        print(payment_intent)
        print(payment_intent['metadata'])
    # ... handle other event types
    else:
        print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    print("Creating checkout session")
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1QwpiRCMpfMOpId7Ti56qhyk',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/payments?success=true',
            cancel_url=YOUR_DOMAIN + '/payments?canceled=true',
            metadata={
                'user_id': "test_id"  # Store user_id in metadata
            }
        )
        print(checkout_session.url)
        return jsonify({'url': checkout_session.url})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=4242)