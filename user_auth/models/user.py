from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager

USER_TYPE = (
    (1, 'Super Admin'),
    (2, 'Sub Admin'),
    (3, 'Customer')
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
    premium_user = models.BooleanField(default=False)
    premium_start_date = models.DateField(null=True, blank=True)
    premium_expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    objects = Manager()
