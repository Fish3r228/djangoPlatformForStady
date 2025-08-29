from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound

from .models import User
from .serializers import (
    UserRegisterSerializer,
    UserSerializer
)


# ===== Регистрация =====
class RegisterAPIView(generics.CreateAPIView):
    """
    Регистрация нового пользователя.
    Доступно без авторизации.
    """
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


# ===== CRUD для пользователей =====
class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD операции для пользователей.
    Обычные пользователи могут видеть/редактировать только свой профиль.
    Админы и staff — всех пользователей.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return User.objects.all()
        return User.objects.filter(pk=user.pk)

    def get_object(self):
        """
        Гарантируем, что обычный пользователь не увидит чужие данные.
        """
        obj = super().get_object()
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            if obj.pk != self.request.user.pk:
                raise NotFound("Пользователь не найден.")
        return obj
