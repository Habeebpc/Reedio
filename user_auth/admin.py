from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user_auth.models import User


class UserAdmin(UserAdmin):
    list_display = ('id', 'name', 'email', 'user_type', 'premium_user')


admin.site.register(User, UserAdmin)