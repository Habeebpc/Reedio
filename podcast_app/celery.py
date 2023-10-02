import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'podcast_app.settings')

app = Celery('podcast_app')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "premium_end_task": {
        "task": "admin_panel.tasks.premium.premium_end_task",
        "schedule": crontab(minute='*/1'),
    }
}
