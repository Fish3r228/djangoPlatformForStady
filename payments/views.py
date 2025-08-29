# payments/views.py
import stripe
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import Payment
from users.serializers import PaymentSerializer
from users.filters import PaymentFilter
from materials.models import Course

# Инициализация Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


# ===== CRUD для платежей =====
class PaymentViewSet(viewsets.ModelViewSet):
    """
    CRUD операции для модели Payment.
    Доступно только авторизованным пользователям.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter


# ===== Создание Stripe-сессии =====
class CreateCheckoutSessionView(APIView):
    """
    Создание Stripe Checkout-сессии для оплаты курса.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        # Получаем курс или возвращаем 404
        course = get_object_or_404(Course, id=course_id)

        # Создаём Stripe-сессию оплаты
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': course.currency,  # берём валюту из модели
                        'product_data': {'name': course.title},
                        'unit_amount': int(course.price * 100),  # цена в центах
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://localhost:8000/success/',
                cancel_url='http://localhost:8000/cancel/',
            )
        except stripe.error.StripeError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

        # Сохраняем платеж в БД
        Payment.objects.create(
            user=request.user,
            course=course,
            stripe_payment_id=session.id,
            amount=course.price,
            status='pending'
        )

        # Возвращаем ссылку на оплату
        return Response({'checkout_url': session.url})
