from celery import shared_task
import datetime
from django.conf import settings
from django.core.management import call_command


@shared_task()
def database_backup():
    try:
        call_command("dbbackup")
        return f"Backed up successfully: {datetime.datetime.now()}"
    except:
        return f"Could not be backed up: {datetime.datetime.now()}"

# @shared_task(name="media_backup")
# def media_backup():
#     try:
#         call_command("mediabackup")
#         return f"Backed up successfully: {datetime.datetime.now()}"
#     except:
#         return f"Could not be backed up: {datetime.datetime.now()}"
