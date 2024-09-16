from celery import shared_task
from user_auth.models import User
from datetime import date
from django.db.models import Q


@shared_task()
def premium_end_task():
    expired_users = User.objects.filter(
        premium_expiry_date__lt=date.today()
    ).filter(
        Q(gold_user=True) | Q(diamond_user=True)
    )
    for user in expired_users:
        user.gold_user = False
        user.diamond_user = False
        user.premium_start_date = None
        user.premium_expiry_date = None
        user.save()
