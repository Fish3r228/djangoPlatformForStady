from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PaymentViewSet, CreateCheckoutSessionView

# ===== Роутер для CRUD платежей =====
router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    # CRUD платежей через роутер
    path('', include(router.urls)),

    # Создание Stripe-сессии для оплаты курса
    path('create-checkout/<int:course_id>/', CreateCheckoutSessionView.as_view(), name='create_checkout'),
]
