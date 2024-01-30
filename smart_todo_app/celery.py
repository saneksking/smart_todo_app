import os
from celery import Celery

from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_todo_app.settings')

app = Celery('smart_todo_app')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'task_test': {
        'task': 'persons.tasks.task_test',
        'schedule': crontab(minute='*'),
    },
}
