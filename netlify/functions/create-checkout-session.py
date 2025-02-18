import os
import json
import stripe

# Get Stripe Secret Key from environment variable
stripe.api_key = 'sk_test_51QjwHnRqYeNsFUyVMdUyRsajmL8FTvxu3c3QnhCbkC0JLbyZsfIDbHvWqGCJDaNsRxAts5PXQiWCPv08ETtIFl5500juYs2S8U'
# stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
if not stripe.api_key:
    print("Stripe secret key not found in environment variables.")
    raise ValueError("Stripe secret key not found in environment variables.")

# Use local domain for testing
DOMAIN = 'https://willy2go.com'

def handler(event, context):
    try:
        # Parse the request body (assuming it's JSON)
        data = json.loads(event['body'])
        big_mac_qty = int(data.get('bigMac', 0))
        mc_nuggets_qty = int(data.get('mcNuggets', 0))

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
            return {
                'statusCode': 400,
                'body': json.dumps("No items selected for checkout.")
            }

        # Create Stripe Checkout Session
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url=DOMAIN + '/success.html?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=DOMAIN + '/cancel.html',
        )

        return {
            'statusCode': 303,
            'headers': {
                'Location': checkout_session.url,
                'Access-Control-Allow-Origin': DOMAIN,  # Allow requests from any origin (for testing)
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST'
            },
            'body': json.dumps({'redirect_url': checkout_session.url})
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
