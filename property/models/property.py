from django.db import models

PROPERTY_TYPES = (
    ('land', 'Land'),
    ('house_flat_villa', 'House/Flat/Villa'),
    ('warehouse', 'Warehouse'),
    ('shop_showroom', 'Shop/Showroom'),
    ('office', 'Office'),
    ('agriculture', 'Agriculture'),
    ('pg', 'PG'),
)
PROPERTY_OPTIONS = (
    ('rent', 'Rent'),
    ('sale', 'Sale'),
    ('both', 'Both'),
    ('lease', 'Lease'),
)
MEASUREMENT_UNITS = (
    ('sqft', 'Sqft'),
    ('acre', 'Acre'),
    ('cent', 'Cent'),
    ('sqm', 'Sq.m'),
    ('sqyrd', 'Sq.yrd'),
    ('sqkm', 'Sq.km'),
    ('sqmile', 'Sq.mile'),
    ('sqinch', 'Sq.inch'),
)


class Property(models.Model):
    created_by = models.ForeignKey('user_auth.User', on_delete=models.SET_NULL,
                                   null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=200, null=True, blank=True)
    customer_address = models.CharField(max_length=200, null=True, blank=True)
    customer_state = models.CharField(max_length=200, null=True, blank=True)
    customer_district = models.CharField(max_length=200, null=True, blank=True)
    customer_pincode = models.CharField(max_length=200, null=True, blank=True)
    customer_phone_number = models.CharField(
        max_length=200, null=True, blank=True)
    relation = models.CharField(max_length=200, null=True, blank=True)

    type = models.CharField(
        max_length=200, null=True, blank=True, choices=PROPERTY_TYPES)
    options = models.CharField(
        max_length=200, null=True, blank=True, choices=PROPERTY_OPTIONS)

    size = models.DecimalField(max_digits=10, decimal_places=2, null=True,
                               blank=True)
    measurement_unit = models.CharField(max_length=200, null=True, blank=True,
                                        choices=MEASUREMENT_UNITS)

    corporation = models.BooleanField(default=False)
    municipality = models.BooleanField(default=False)
    village = models.BooleanField(default=False)
    panchayat = models.BooleanField(default=False)
    location = models.CharField(max_length=200, null=True, blank=True)
    taluk = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    district = models.CharField(max_length=200, null=True, blank=True)
    pincode = models.CharField(max_length=200, null=True, blank=True)
    landmark = models.CharField(max_length=200, null=True, blank=True)
    zoning = models.CharField(max_length=200, null=True, blank=True)
    natural_element_present_in_site = models.CharField(
        max_length=200, null=True, blank=True)
    water_source = models.CharField(max_length=200, null=True, blank=True)
    google_location_url = models.URLField(
        max_length=500, null=True, blank=True)

    owner_name = models.CharField(max_length=200, null=True, blank=True)
    owner_personal_address = models.CharField(
        max_length=200, null=True, blank=True)
    owner_state = models.CharField(max_length=200, null=True, blank=True)
    owner_district = models.CharField(max_length=200, null=True, blank=True)
    owner_pincode = models.CharField(max_length=200, null=True, blank=True)
    owner_phone_number = models.CharField(
        max_length=200, null=True, blank=True)
    ownership = models.CharField(max_length=200, null=True, blank=True)

    survey_plan = models.URLField(null=True, blank=True)
    area_plan = models.URLField(null=True, blank=True)
    adhaar_copy = models.URLField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
