from rest_framework import serializers
from auth_app.models import CustomUser
from facilities.serializers import GymSerializer


class UserSerializer(serializers.ModelSerializer):
    gym = GymSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'contact_number', 'gym']

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update user details without handling facilities
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.contact_number = validated_data.get('contact_number', instance.contact_number)
        instance.save()
        return instance