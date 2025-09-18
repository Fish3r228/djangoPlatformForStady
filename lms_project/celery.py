import os
from celery import Celery   # <-- правильно импортируем Celery из пакета celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms_project.settings")

app = Celery("lms_project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
