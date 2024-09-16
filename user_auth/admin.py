from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user_auth.models import User, PartnerAndRetailer


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
                    'gold_user',
                    'diamond_user',
                    'premium_start_date',
                    'premium_expiry_date'
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
    list_display = ('id', 'name', 'email', 'user_type', 'gold_user', 'diamond_user')


admin.site.register(User, UserAdmin)
admin.site.register(PartnerAndRetailer)