from django.urls import path
from .views import GymListCreateView, GymDetailView,GymPhotoUploadView, GymsWithinRadiusView

urlpatterns = [
    path('gyms/', GymListCreateView.as_view(), name='gym-list-create'),
    path('gyms/<int:pk>/', GymDetailView.as_view(), name='gym-detail'),
    path('gyms-within-radius/', GymsWithinRadiusView.as_view(), name='gyms-within-radius'),
    path('gym/upload-photo', GymPhotoUploadView.as_view(), name="gym-photo" )
]
