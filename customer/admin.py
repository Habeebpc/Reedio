from django.contrib import admin
from customer.models import (
    Favorite,
    FavoriteAudio,
    AudioProgress,
    PurchasePodcast
)

admin.site.register(Favorite)
admin.site.register(FavoriteAudio)
admin.site.register(PurchasePodcast)


class AudioProgressAdmin(admin.ModelAdmin):
    list_display = ('audio', 'user', 'progress')


admin.site.register(AudioProgress, AudioProgressAdmin)
