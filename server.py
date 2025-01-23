# import os
# from flask import Flask, redirect, request

# import stripe

# stripe.api_key = 'sk_test_51QjwHnRqYeNsFUyVMdUyRsajmL8FTvxu3c3QnhCbkC0JLbyZsfIDbHvWqGCJDaNsRxAts5PXQiWCPv08ETtIFl5500juYs2S8U'

# app = Flask(__name__,
#             static_url_path='/static',
#             static_folder='public')

# DOMAIN = 'https://willy2go.github.io/Willy2Go/'

# @app.route('/create-checkout-session', methods=['POST'])
# def create_checkout_session():
#     try:
#         # Retrieve the form data
#         big_mac_qty = int(request.form.get('bigMac', 0))
#         mc_nuggets_qty = int(request.form.get('mcNuggets', 0))
#         fries_large_qty = int(request.form.get('friesLarge', 0))
#         fries_small_qty = int(request.form.get('friesSmall', 0))
#         drinks_qty = int(request.form.get('drinks', 0))
        
#         # Define the product prices
#         prices = {
#             'bigMac': 5.99,
#             'mcNuggets': 4.99,
#             'friesLarge': 2.99,
#             'friesSmall': 1.99,
#             'drinks': 1.49
#         }

#         # Create a list of line items based on the quantities and prices
#         line_items = []
#         if big_mac_qty > 0:
#             line_items.append({
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {
#                         'name': 'Big Mac',
#                     },
#                     'unit_amount': int(prices['bigMac'] * 100),  # Stripe expects amount in cents
#                 },
#                 'quantity': big_mac_qty,
#             })
#         if mc_nuggets_qty > 0:
#             line_items.append({
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {
#                         'name': 'Chicken McNuggets',
#                     },
#                     'unit_amount': int(prices['mcNuggets'] * 100),
#                 },
#                 'quantity': mc_nuggets_qty,
#             })
#         if fries_large_qty > 0:
#             line_items.append({
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {
#                         'name': 'Large French Fries',
#                     },
#                     'unit_amount': int(prices['friesLarge'] * 100),
#                 },
#                 'quantity': fries_large_qty,
#             })
#         if fries_small_qty > 0:
#             line_items.append({
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {
#                         'name': 'Small French Fries',
#                     },
#                     'unit_amount': int(prices['friesSmall'] * 100),
#                 },
#                 'quantity': fries_small_qty,
#             })
#         if drinks_qty > 0:
#             line_items.append({
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {
#                         'name': 'Sprite',
#                     },
#                     'unit_amount': int(prices['drinks'] * 100),
#                 },
#                 'quantity': drinks_qty,
#             })

#         # Create the checkout session
#         checkout_session = stripe.checkout.Session.create(
#             line_items=line_items,
#             mode='payment',
#             success_url=DOMAIN,
#             cancel_url=DOMAIN,
#             # success_url=YOUR_DOMAIN + '/success.html',
#             # cancel_url=YOUR_DOMAIN + '/cancel.html',
#         )
#     except Exception as e:
#         return str(e)

#     return redirect(checkout_session.url, code=303)

# if __name__ == '__main__':
#     app.run()






#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, redirect, request

import stripe
# This is your test secret API key.
stripe.api_key = 'sk_test_51QjwHnRqYeNsFUyVMdUyRsajmL8FTvxu3c3QnhCbkC0JLbyZsfIDbHvWqGCJDaNsRxAts5PXQiWCPv08ETtIFl5500juYs2S8U'

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

YOUR_DOMAIN = 'http://localhost:4242'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': '{{PRICE_ID}}',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

if __name__ == '__main__':
    app.run(port=4242)
