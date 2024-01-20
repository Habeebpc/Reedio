from django.contrib import admin
from customer.models import Favorite, FavoriteAudio, AudioProgress

admin.site.register(Favorite)
admin.site.register(FavoriteAudio)
admin.site.register(AudioProgress)
