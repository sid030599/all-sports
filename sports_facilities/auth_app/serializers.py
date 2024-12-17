from rest_framework import serializers
from auth_app.models import CustomUser
from facilities.serializers import FacilitySerializer


class UserSerializer(serializers.ModelSerializer):
    # Include the list of facilities owned by the user
    facilities = FacilitySerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'contact_number', 'facilities']
