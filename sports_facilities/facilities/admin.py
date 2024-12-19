from django.contrib import admin
from .models import Gym, GymPhoto, GymMember, GymTrainer, GymFeature, GymSubscriptionPlan, GymRatingReview

# Register the Facility model
admin.site.register(Gym)
admin.site.register(GymPhoto)
admin.site.register(GymTrainer)
admin.site.register(GymMember)
admin.site.register(GymFeature)
admin.site.register(GymSubscriptionPlan)
admin.site.register(GymRatingReview)