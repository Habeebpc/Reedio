from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user_auth.models import User


class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            ('Personal info'),
            {
                'fields': (
                    'name',
                    'email',
                    'mobile',
                    'premium_user'
                )
            }
        ),

        (
            ('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'user_type'
                )
            }
        ),
        (('Important dates'), {'fields': ('last_login',)}))
    list_display = ('id', 'name', 'email', 'user_type', 'premium_user')


admin.site.register(User, UserAdmin)
