from celery import shared_task
from user_auth.models import User
from datetime import date


@shared_task()
def premium_end_task():
    expired_users = User.objects.filter(
        premium_user=True, premium_expiry_date__lt=date.today())
    for user in expired_users:
        user.premium_user = False
        user.save(update_fields=['premium_user'])
