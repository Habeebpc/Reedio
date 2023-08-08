from django.db import models


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
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)

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
