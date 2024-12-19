from rest_framework import serializers
from .models import Gym, GymPhoto
from auth_app.serializers import UserSerializer


class GymPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymPhoto
        fields = ["id", "photo", "uploaded_at"]


class GymSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gym
        fields = [
            "id",
            "name",
            "description",
            "location",
            "contact_number",
            "price_range",
            "logo",
        ]


class GymDetailSerializer(GymSerializer):
    photos = GymPhotoSerializer(many=True, read_only=True)
    owner = UserSerializer()

    class Meta:
        model = Gym
        fields = [
            "address",
            "photos",
            "owner",
            "average_rating",
            "review_count"
        ]
