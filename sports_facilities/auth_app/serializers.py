from rest_framework import serializers
from auth_app.models import CustomUser
from facilities.models import GymMember, GymTrainer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "role", "contact_number", "password"]

    def create(self, validated_data):
        password = validated_data.pop('password')  # Extract password
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)  # Hash the password and set it
        user.save()
        return user

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
    user_details = UserSerializer(source="user", read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), write_only=True
    )

    class Meta:
        model = GymMember
        fields = [
            "id",
            "user",
            "user_details",
            "gym",
            "subscription_plan",
            "subscription_start_date",
            "subscription_end_date",
            "subscription_type",
            "goals",
        ]

    def validate(self, data):
        # Ensure subscription_end_date is after subscription_start_date
        if data["subscription_end_date"] <= data["subscription_start_date"]:
            raise serializers.ValidationError("Subscription end date must be after start date.")
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)
    
class TrainerSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source="user", read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), write_only=True
    )

    class Meta:
        model = GymTrainer
        fields = [
            "id",
            "user",
            "user_details",
            "gym",
            "specialization",
            "certification",
            "years_of_experience",
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)