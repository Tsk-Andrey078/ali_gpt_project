# myproject/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ali_rest.settings')

app = Celery('ali_rest')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находит все задачи (tasks) в приложениях Django
app.autodiscover_tasks()
