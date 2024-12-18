from django.contrib.gis.db import models
from auth_app.models import CustomUser

# Gym model for gym owners
class Gym(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='gyms', limit_choices_to={'role': 'owner'})
    name = models.CharField(max_length=255)
    address = models.TextField()
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    price_range = models.CharField(max_length=50, blank=True, null=True)
    equipment = models.JSONField(blank=True, null=True)
    trainers = models.JSONField(blank=True, null=True)
    subscription_pricing = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Member(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='membership')
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='members')
    membership_start_date = models.DateField()
    membership_end_date = models.DateField()
    membership_type = models.CharField(max_length=50, choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')])
    contact_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.gym.name}"

class GymPhoto(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='gym_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo of {self.gym.name}"