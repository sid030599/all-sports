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
    path("lists/", GymListView.as_view(), name="gym-list-create"),
    path("details", GymDetailView.as_view(), name="gym-detail"),
    path(
        "nearby/", GymsWithinRadiusView.as_view(), name="gyms-within-radius"
    ),
    path("upload-photo", GymPhotoUploadView.as_view(), name="gym-photo"),
    path(
        "subscription-plans/",
        GymSubscriptionPlanView.as_view(),
        name="gym-subscription-plans",
    ),
    path(
        "reviews/",
        GymRatingReviewView.as_view(),
        name="gym-reviews",
    ),
    path("features/", GymFeatureView.as_view(), name="gym-features"),
    path("members/", GymMemberView.as_view(), name="gym-members"),
    path("trainers/", GymTrainerView.as_view(), name="gym-trainers"),
]
