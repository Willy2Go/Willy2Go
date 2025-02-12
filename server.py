import os
from flask import Flask, redirect, request
import stripe

# Stripe Secret Key (Make sure this is secure and NOT hardcoded in production)
stripe.api_key = 'sk_test_51QjwHnRqYeNsFUyVMdUyRsajmL8FTvxu3c3QnhCbkC0JLbyZsfIDbHvWqGCJDaNsRxAts5PXQiWCPv08ETtIFl5500juYs2S8U'

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

# Use local domain for testing
# DOMAIN = 'http://localhost:4242'
DOMAIN = 'https://willy2go.github.io/Willy2Go/'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        big_mac_qty = int(request.form.get('bigMac', 0))
        mc_nuggets_qty = int(request.form.get('mcNuggets', 0))

        line_items = []

        if big_mac_qty > 0:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'Big Mac'},
                    'unit_amount': 599,  # Price in cents
                },
                'quantity': big_mac_qty,
            })

        if mc_nuggets_qty > 0:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'McNuggets'},
                    'unit_amount': 499,  # Price in cents
                },
                'quantity': mc_nuggets_qty,
            })

        # Ensure line_items is not empty
        if not line_items:
            return "No items selected for checkout."

        # Create Stripe Checkout Session
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            # success_url=DOMAIN + '/success.html',
            # cancel_url=DOMAIN + '/cancel.html',
        )

    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

if __name__ == '__main__':
    app.run(port=4242, debug=True)
