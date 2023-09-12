from django.contrib import admin
from admin_panel.models import (
    Category,
    SubCategory,
    Podcast,
    PlayList,
    Banner,
    DummyImage,
    Settings
)

# Register your models here.

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Podcast)
admin.site.register(PlayList)
admin.site.register(Banner)
admin.site.register(DummyImage)
admin.site.register(Settings)
