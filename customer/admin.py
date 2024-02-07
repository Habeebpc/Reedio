from django.contrib import admin
from customer.models import Favorite, FavoriteAudio, AudioProgress

admin.site.register(Favorite)
admin.site.register(FavoriteAudio)


class AudioProgressAdmin(admin.ModelAdmin):
    list_display = ('audio', 'user', 'progress')


admin.site.register(AudioProgress, AudioProgressAdmin)