from django.urls import path
from .views import (
    GymListView,
    GymDetailView,
    GymPhotoUploadView,
    GymsWithinRadiusView,
    GymRatingReviewView,
    GymSubscriptionPlanView,
    GymFeatureView,
    GymMemberView,
    GymTrainerView
)

urlpatterns = [
    path("gyms/", GymListView.as_view(), name="gym-list-create"),
    path("gym/details", GymDetailView.as_view(), name="gym-detail"),
    path(
        "gyms-within-radius/", GymsWithinRadiusView.as_view(), name="gyms-within-radius"
    ),
    path("gym/upload-photo", GymPhotoUploadView.as_view(), name="gym-photo"),
    path(
        "gyms/subscription-plans/",
        GymSubscriptionPlanView.as_view(),
        name="gym-subscription-plans",
    ),
    path(
        "gyms/reviews/",
        GymRatingReviewView.as_view(),
        name="gym-reviews",
    ),
    path("gym/features/", GymFeatureView.as_view(), name="gym-features"),
    path("gym/members/", GymMemberView.as_view(), name="gym-members"),
    path("gym/trainers/", GymTrainerView.as_view(), name="gym-trainers"),
]
