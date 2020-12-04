import os
from celery import Celery, shared_task
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'duplicate_site.settings.base')

app = Celery('duplicate_site')

app.config_from_object('django.conf:settings', namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_every_midnight': {
        'task': 'duplicate.tasks.find_duplicates',
        'schedule': crontab(minute=0,hour=0),
    },
}