from django.db import models


class Meeting(models.Model):
    created_by = models.ForeignKey('user_auth.User', on_delete=models.SET_NULL,
                                   null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    meeting_date = models.DateTimeField()
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    agenda = models.TextField(null=True, blank=True)
    place = models.CharField(max_length=200, null=True, blank=True)
    minutes = models.TextField(null=True, blank=True)
    document = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name
