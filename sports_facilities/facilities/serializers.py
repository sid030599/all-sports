from rest_framework import serializers
from .models import Gym, Member

# Gym Serializer
class GymSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Gym
        fields = ['id', 'owner', 'name', 'address', 'location', 'contact_number', 'price_range', 'equipment', 'trainers', 'subscription_pricing', 'created_at']


# Member Serializer
class MemberSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    gym = GymSerializer(read_only=True)

    class Meta:
        model = Member
        fields = ['id', 'user', 'gym', 'membership_start_date', 'membership_end_date', 'membership_type', 'contact_number']
