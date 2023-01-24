import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager


class Manager(UserManager):

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields['is_superuser'] = True
        super(Manager, self).create_superuser(username, email, password,
                                              **extra_fields)


class User(AbstractUser):
    name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=12)
    designation = models.CharField(max_length=200, null=True, blank=True)
    profile_photo = models.URLField(null=True, blank=True)
    is_blocked_user = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    objects = Manager()
