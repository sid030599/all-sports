from rest_framework import serializers
from auth_app.models import CustomUser
from facilities.models import GymMember


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "role", "contact_number"]

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update user details without handling facilities
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.role = validated_data.get("role", instance.role)
        instance.contact_number = validated_data.get(
            "contact_number", instance.contact_number
        )
        instance.save()
        return instance


class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GymMember
        fields = [
            "id",
            "user",
            "subscription_plan",
            "subscription_end_date",
            "subscription_type",
            "goals",
        ]
