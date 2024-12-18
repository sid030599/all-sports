from django.contrib import admin
from .models import Gym, GymPhoto

# Register the Facility model
admin.site.register(Gym)
admin.site.register(GymPhoto)