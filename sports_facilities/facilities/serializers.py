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
        fields = ["id", "photo", "created_at"]
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)


class GymSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gym
        fields = [
            "id",
            "name",
            "description",
            "location",
            "contact_number",
            "standard",
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

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)

    def udpate(self, validated_data):
        request = self.context.get('request')
        validated_data['updated_by'] = request.user
        return super().update(validated_data)


class GymRatingReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymRatingReview
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at",
            "updated_by",
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)


class GymFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymFeature
        fields = "__all__"
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)


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
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        subscription_plan = GymSubscriptionPlan.objects.create(**validated_data)
        subscription_plan.features.set(features)
        return subscription_plan

    def update(self, instance, validated_data):
        features = validated_data.pop("features", None)
        request = self.context.get('request')
        validated_data['updated_by'] = request.user
        if features is not None:
            instance.features.set(features)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
