from rest_framework import serializers
from .models import (
    Gym,
    GymPhoto,
    GymFeature,
    GymSubscriptionPlan,
    GymRatingReview
)
from jsonschema import validate
from drf_spectacular.utils import extend_schema_field, OpenApiTypes


class GymIdValidationSerializer(serializers.Serializer):
    gym_id = serializers.IntegerField()

    def validate_gym_id(self, value):
        if not Gym.objects.filter(id=value).exists():
            raise serializers.ValidationError("Gym with this id does not exist.")
        return value


class GymPhotoSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField()

    class Meta:
        model = GymPhoto
        fields = ["id", "photo", "created_at", "gym", "description", "video"]

    def validate(self, attrs):
        gym = attrs.get("gym")
        if not gym:
            raise serializers.ValidationError({"gym": "A valid gym is required."})

        if "photo" not in self.initial_data:
            raise serializers.ValidationError({"photo": "No photo provided."})

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["created_by"] = request.user
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
            "address",
        ]


from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from jsonschema import validate

ADDRESS_SCHEMA = {
    "type": "object",
    "properties": {
        "street": {"type": "string", "default": ""},
        "city": {"type": "string", "default": ""},
        "state": {"type": "string", "maxLength": 50, "default": ""},
        "zip_code": {"type": "string", "default": ""},
        "country": {"type": "string", "minLength": 1, "default": "India"},
    },
    "required": ["street", "city", "state", "zip_code", "country"],
    "additionalProperties": False,
}

def apply_defaults(data, schema):
    """Recursively apply default values from schema."""
    if "default" in schema:
        data = data or schema["default"]
    if schema.get("type") == "object" and "properties" in schema:
        data = data or {}
        for key, subschema in schema["properties"].items():
            if key not in data:
                data[key] = apply_defaults(None, subschema)
            else:
                data[key] = apply_defaults(data[key], subschema)
    return data

class GymDetailSerializer(GymSerializer):
    photos = GymPhotoSerializer(many=True, read_only=True)

    class Meta(GymSerializer.Meta):
        model = Gym
        fields = GymSerializer.Meta.fields + [
            "owner",
            "photos",
            "owner",
            "average_rating",
            "review_count",
        ]
        read_only_fields = [
            "average_rating",
            "review_count",
        ]

    # Apply schema validation to address field
    def validate_address(self, value):
        # Apply JSON schema validation
        try:
            value = apply_defaults(value, ADDRESS_SCHEMA)
            validate(instance=value, schema=ADDRESS_SCHEMA)
            return value
        except Exception as e:
            raise serializers.ValidationError(f"Invalid address: {e}")

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["created_by"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        validated_data["updated_by"] = request.user
        return super().update(instance, validated_data)


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
        request = self.context.get("request")
        validated_data["created_by"] = request.user
        return super().create(validated_data)


class GymFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymFeature
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["created_by"] = request.user
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
        request = self.context.get("request")
        validated_data["created_by"] = request.user
        subscription_plan = GymSubscriptionPlan.objects.create(**validated_data)
        subscription_plan.features.set(features)
        return subscription_plan

    def update(self, instance, validated_data):
        features = validated_data.pop("features", None)
        request = self.context.get("request")
        validated_data["updated_by"] = request.user
        if features is not None:
            instance.features.set(features)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
