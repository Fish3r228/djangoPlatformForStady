from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, UserRegisterView, UserViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'', UserViewSet, basename='user')  # пустая строка!

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegisterView.as_view(), name='user-register'),
]
