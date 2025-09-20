from lms_project.celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Course

@shared_task
def send_course_update_email(course_id, emails):
    """
    Асинхронная задача для отправки письма подписчикам об обновлении курса
    """
    course = Course.objects.get(id=course_id)
    send_mail(
        subject=f"Обновление по курсу {course.title}",
        message=f"Курс '{course.title}' был обновлен. Зайдите, чтобы посмотреть новые материалы.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=emails,
    )
