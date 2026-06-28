from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Driver


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )

    class Meta:
        model = Driver
        fields = ['id', 'user', 'user_id', 'license_number', 'phone', 'status', 'created_at', 'updated_at']
