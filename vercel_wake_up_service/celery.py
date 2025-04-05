import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vercel_wake_up_service.settings')
app = Celery('vercel_wake_up_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

CELERY_BEAT_SCHEDULE = {
    'ping-vercel-sites-every-minute': {
        'task': 'server.tasks.ping_all_sites',
        'schedule': crontab(minute='*/1'),
    },
    'daily-website-report-email': {
        'task': 'myproject.tasks.daily_site_report',
        'schedule': crontab(hour='*/24'),
    },
}