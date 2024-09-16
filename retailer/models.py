from django.db import models

# Create your models here.


class AccessCode(models.Model):
    created_by = models.ForeignKey(
        "user_auth.User",
        on_delete=models.CASCADE, related_name="access_codes_created_by"
    )
    podcast = models.ForeignKey(
        "admin_panel.Podcast",
        on_delete=models.CASCADE, related_name="access_codes"
    )
    redeemed_by = models.ForeignKey(
        "user_auth.User",
        on_delete=models.CASCADE, related_name="access_codes_redeemed_by",
        null=True, blank=True
    )
    code = models.CharField(max_length=15)
    sent_to = models.CharField(max_length=13, null=True, blank=True)
    validity = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    redeemed_on = models.DateTimeField(null=True, blank=True)
