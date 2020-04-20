from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inv_web.settings')

app = Celery('inv_web')

class Config:
    enable_utc = True
    timezone = 'Asia/Kuala_Lumpur'
    broker_url = 'amqp://localhost'
    beat_schedule = {
    'status-daily-update': {
        'task': 'invoices.tasks.update_status',
        'schedule': crontab(minute=0, hour=0),
        # 'schedule': crontab(minute='*/10'),
        },
    }

app.config_from_object(Config)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()