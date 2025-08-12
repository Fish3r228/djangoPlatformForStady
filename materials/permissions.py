from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and
                    request.user.groups.filter(name='moderators').exists())

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешаем безопасные методы (GET, HEAD, OPTIONS) всем
        if request.method in SAFE_METHODS:
            return obj.owner == request.user
        # Для изменения, удаления — только владелец
        return obj.owner == request.user