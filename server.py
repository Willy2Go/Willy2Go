#! /usr/bin/env python3.6

import os
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
import stripe

# Stripe Secret Key (Make sure this is secure and NOT hardcoded in production)
stripe.api_key = 'sk_test_51QjwHnRqYeNsFUyVMdUyRsajmL8FTvxu3c3QnhCbkC0JLbyZsfIDbHvWqGCJDaNsRxAts5PXQiWCPv08ETtIFl5500juYs2S8U'

# app = Flask(__name__,
#             static_url_path='',
#             static_folder='public')

app = Flask(__name__)
CORS(app, resources={r"/create-checkout-session": {"origins": ["https://willy2go.com", "http://localhost:4242"]}})


# Use local domain for testing
# DOMAIN = 'http://localhost:4242'
# DOMAIN = 'https://willy2go.github.io/Willy2Go'
# DOMAIN = 'http://127.0.0.1:3000/index.html'
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

if __name__ == '__main__':
    app.run(port=4242, debug=True)
    # app.run()
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)