from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager

USER_TYPE = (
    (1, 'Super Admin'),
    (2, 'Sub Admin'),
    (3, 'Customer'),
    (4, 'Partner'),
    (5, 'Retailer')
)


class Manager(UserManager):

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields['is_superuser'] = True
        extra_fields['user_type'] = 1
        super(Manager, self).create_superuser(username, email, password,
                                              **extra_fields)


class User(AbstractUser):
    name = models.CharField(max_length=200)
    mobile = models.CharField(
        max_length=12, unique=True, null=True, blank=True)
    user_type = models.PositiveBigIntegerField(choices=USER_TYPE)
    gold_user = models.BooleanField(default=False)
    diamond_user = models.BooleanField(default=False)
    premium_start_date = models.DateField(null=True, blank=True)
    premium_expiry_date = models.DateField(null=True, blank=True)
    audio_permission = models.BooleanField(default=False)
    validity = models.DateField(null=True, blank=True)

    objects = Manager()


class PartnerAndRetailer(models.Model):
    partner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='partners'
    )
    retailer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='retailers'
    )
    name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=12, null=True, blank=True)
    email = models.EmailField()
    is_active = models.BooleanField(default=False)
