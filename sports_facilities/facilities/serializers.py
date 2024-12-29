from rest_framework import serializers
from .models import (
    Gym,
    GymPhoto,
    GymFeature,
    GymSubscriptionPlan,
    GymRatingReview,
    GymMember,
    GymTrainer,
)


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

    class Meta(GymSerializer.Meta):
        model = Gym
        fields = GymSerializer.Meta.fields + [
            "owner",
            "address",
            "photos",
            "owner",
            "average_rating", "review_count",
        ]
        read_only_fields = ["average_rating", "review_count",]

class GymRatingReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymRatingReview
        fields = "__all__"


class GymFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymFeature
        fields = "__all__"


class GymSubscriptionPlanSerializer(serializers.ModelSerializer):
    features = serializers.PrimaryKeyRelatedField(
        queryset=GymFeature.objects.all(), many=True, write_only=True
    )
    feature_details = GymFeatureSerializer(source="features", many=True, read_only=True)

    class Meta:
        model = GymSubscriptionPlan
        fields = "__all__"

    def create(self, validated_data):
        features = validated_data.pop("features", [])
        subscription_plan = GymSubscriptionPlan.objects.create(**validated_data)
        subscription_plan.features.set(features)
        return subscription_plan

    def update(self, instance, validated_data):
        features = validated_data.pop("features", None)
        if features is not None:
            instance.features.set(features)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

