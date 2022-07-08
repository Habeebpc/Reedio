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
   
    def __str__(self):
        return self.username

    objects = Manager()


class AbstractModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(
        "user_auth.User", blank=True, null=True,
        related_name="creator_%(class)s_objects",
        on_delete=models.SET_NULL)
    updater = models.ForeignKey(
        "user_auth.User", blank=True, null=True,
        related_name="updater_%(class)s_objects",
        on_delete=models.SET_NULL)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
