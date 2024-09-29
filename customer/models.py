from django.db import models


class Favorite(models.Model):
    user = models.ForeignKey(
        'user_auth.User', on_delete=models.CASCADE, related_name='favorites')
    podcast = models.ForeignKey(
        'admin_panel.Podcast',
        on_delete=models.CASCADE, related_name='favorites')
    added_on = models.DateTimeField(auto_now_add=True)


class FavoriteAudio(models.Model):
    user = models.ForeignKey(
        'user_auth.User',
        on_delete=models.CASCADE, related_name='favorite_audios')
    playlist = models.ForeignKey(
        'admin_panel.PlayList',
        on_delete=models.CASCADE, related_name='favorite_audios')
    added_on = models.DateTimeField(auto_now_add=True)


class AudioProgress(models.Model):
    user = models.ForeignKey(
        'user_auth.User',
        on_delete=models.CASCADE, related_name='audio_progresses')
    audio = models.ForeignKey(
        'admin_panel.PlayList',
        on_delete=models.CASCADE, related_name='audio_progresses')
    progress = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)


class HelpDesk(models.Model):
    user = models.ForeignKey(
        'user_auth.User', on_delete=models.CASCADE, related_name='help_desk')
    title = models.CharField(max_length=100)
    body = models.TextField(null=True, blank=True)
    reply = models.TextField(null=True, blank=True)
    is_replied = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    reply_on = models.DateTimeField(null=True, blank=True)


class PurchasePodcast(models.Model):
    user = models.ForeignKey(
        'user_auth.User', on_delete=models.CASCADE, related_name='purchases')
    podcast = models.ForeignKey(
        'admin_panel.Podcast',
        on_delete=models.CASCADE, related_name='purchases')
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
