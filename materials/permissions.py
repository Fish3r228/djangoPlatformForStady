from rest_framework.permissions import BasePermission, SAFE_METHODS

class CourseLessonPermission(BasePermission):
    """
    Правила доступа:
    - Модераторы видят и могут редактировать все.
    - Обычные пользователи видят и редактируют только свои объекты.
    - Чтение разрешено всем аутентифицированным.
    """

    def has_permission(self, request, view):
        # Все аутентифицированные могут видеть список и создавать
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Разрешаем безопасные методы всем аутентифицированным
        if request.method in SAFE_METHODS:
            return True

        # Модераторы могут всё
        if request.user.groups.filter(name='moderators').exists():
            return True

        # Иначе — только владелец объекта
        return obj.owner == request.user
