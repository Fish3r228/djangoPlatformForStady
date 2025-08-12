# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterAPIView, UserViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('', include(router.urls)),
]
