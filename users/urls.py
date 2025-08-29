from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import RegisterAPIView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('', include(router.urls)),
]
