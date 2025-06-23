import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booking_project.settings')

app = Celery('booking_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-event-reminders': {
        'task': 'booking.tasks.send_event_reminders',
        'schedule': crontab(minute='*/5'),
    },
    'cleanup-old-events': {
        'task': 'booking.tasks.cleanup_old_events',
        'schedule': crontab(hour=2, minute=0),
    },
}