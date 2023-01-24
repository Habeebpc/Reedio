from django.db import models


class Plot(models.Model):
    created_by = models.ForeignKey('user_auth.User', on_delete=models.SET_NULL,
                                   null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=200, null=True, blank=True)
    personal_address = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    district = models.CharField(max_length=200, null=True, blank=True)
    pincode = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    property_relation = models.CharField(max_length=200, null=True, blank=True)

    property_type = models.CharField(max_length=200, null=True, blank=True,)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    area = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True,
                                blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.CharField(max_length=200, null=True, blank=True)
    longitude = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class PlotImage(models.Model):
    plot = models.ForeignKey('plot.Plot', on_delete=models.CASCADE)
    image = models.URLField(max_length=500)

    def __str__(self):
        return self.plot.name
