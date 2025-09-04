from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def deactivate_inactive_users():
    """Блокирует пользователей, которые не заходили более 30 дней"""
    threshold = now() - timedelta(days=30)
    users = User.objects.filter(last_login__lt=threshold, is_active=True)
    users.update(is_active=False)
