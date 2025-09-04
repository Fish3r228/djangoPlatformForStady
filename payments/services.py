import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(course, success_url, cancel_url):
    """
    Создание Stripe Checkout Session для оплаты курса.
    Возвращает объект сессии Stripe.
    """
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': course.title},
                'unit_amount': int(course.price * 100),  # цена в центах
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session
