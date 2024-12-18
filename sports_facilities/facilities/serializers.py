from rest_framework import serializers
from .models import Gym, Member, GymPhoto

class GymPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymPhoto
        fields = ['id', 'photo', 'uploaded_at']
        
class GymSerializer(serializers.ModelSerializer):
    photos = GymPhotoSerializer(many=True, read_only=True)
    class Meta:
        model = Gym
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 'location', 'contact_number', 'price_range', 'equipment', 'trainers', 'subscription_pricing', 'photos']

# Member Serializer
class MemberSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    gym = GymSerializer(read_only=True)

    class Meta:
        model = Member
        fields = ['id', 'user', 'gym', 'membership_start_date', 'membership_end_date', 'membership_type', 'contact_number']


