from rest_framework import serializers
from .models import Facility

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['id', 'name', 'type', 'address', 'location', 'amenities', 'contact_number', 'price_range', 'extra_info', 'owner', 'created_at']
