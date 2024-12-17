from django.urls import path
from .views import FacilityListAPIView, FacilityDetailAPIView

urlpatterns = [
    path('facilities/', FacilityListAPIView.as_view(), name='facility-list'),
    path('facilities/<int:pk>/', FacilityDetailAPIView.as_view(), name='facility-detail'),
]
