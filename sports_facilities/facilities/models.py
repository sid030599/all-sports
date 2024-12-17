from django.contrib.gis.db import models
from auth_app.models import CustomUser

class Facility(models.Model):
    FACILITY_TYPES = [
        ('gym', 'Gym'),
        ('pool', 'Swimming Pool'),
        ('club', 'Sports Club'),
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=FACILITY_TYPES)
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    amenities = models.JSONField(null=True, blank=True)  # Common amenities
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    price_range = models.CharField(max_length=50, null=True, blank=True)
    extra_info = models.JSONField(null=True, blank=True)  # Type-specific data
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_facilites')

    def __str__(self):
        return self.name
