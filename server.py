#! /usr/bin/env python3.6

import os
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
import stripe
from dotenv import load_dotenv

load_dotenv()

# Stripe Secret Key (Make sure this is secure and NOT hardcoded in production)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

if not stripe.api_key:
    raise ValueError("Missing STRIPE_SECRET_KEY in environment variables")

app = Flask(__name__)
CORS(app, resources={
    r"/create-checkout-session": {"origins": ["https://willy2go.com", "http://localhost:4242"]},
    r"/emailjs-config": {"origins": ["https://willy2go.com", "http://localhost:4242"]}
})

DOMAIN = 'https://willy2go.com'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.json  # Extract JSON from frontend request
        items = data.get("items", [])

        # Validate items
        if not items:
            return jsonify({"error": "No items selected for checkout"}), 400

        line_items = [
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": item["name"]},
                    "unit_amount": int(item["price"] * 100),  # Convert dollars to cents
                },
                "quantity": item["quantity"],
            }
            for item in items
        ]

        # Create Stripe Checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=DOMAIN + '/success.html',  # Redirect after successful payment
            cancel_url=DOMAIN + '/cancel.html',    # Redirect if payment is canceled
        )


        return jsonify({"url": checkout_session.url})  # Send session URL to frontend

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/emailjs-config')
def emailjs_config():
    config = {
        "service_id": os.getenv("EMAILJS_SERVICE_ID"),
        "template_id": os.getenv("EMAILJS_TEMPLATE_ID"),
        "user_id": os.getenv("EMAILJS_USER_ID"),
    }
    print("Serving EmailJS Config:", config)  # Debugging: Check if user_id is present
    return jsonify(config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
