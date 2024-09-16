from django.db import models

APP_STATUS = (
    ('active', 'Active'),
    ('under_maintenance', 'Under Maintenance')
)


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    icon = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    icon = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Podcast(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    created_by = models.ForeignKey(
        'user_auth.User',
        on_delete=models.SET_NULL,
        null=True, blank=True, related_name='podcasts')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    price = models.FloatField(null=True, blank=True)
    is_gold = models.BooleanField(default=False)
    is_diamond = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class PlayList(models.Model):
    podcast = models.ForeignKey(
        Podcast, on_delete=models.CASCADE, related_name='play_lists')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    audio_url = models.URLField()
    sub_required = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)
    position = models.FloatField(default=0)
    is_trashed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Banner(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    redirect_url = models.URLField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DummyImage(models.Model):
    image = models.URLField(null=True, blank=True)
    redirect_url = models.URLField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image


class Settings(models.Model):
    app_status = models.CharField(
        max_length=30, choices=APP_STATUS, default='active')


class Package(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    validity = models.IntegerField()
