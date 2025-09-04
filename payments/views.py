# payments/views.py
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Payment
from users.serializers import PaymentSerializer
from materials.models import Course
from .services import create_checkout_session


class PaymentViewSet(viewsets.ModelViewSet):
    """
    CRUD для платежей
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class CreateCheckoutSessionView(APIView):
    """
    Создание Stripe Checkout-сессии для оплаты курса.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        # Создаём Stripe-сессию через сервис
        session = create_checkout_session(
            course,
            success_url="http://localhost:8000/success/",
            cancel_url="http://localhost:8000/cancel/",
        )

        # Сохраняем платеж в БД
        Payment.objects.create(
            user=request.user,
            course=course,
            stripe_payment_id=session.id,
            amount=course.price,
            status='pending'
        )

        return Response({"checkout_url": session.url})
