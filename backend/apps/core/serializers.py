import re

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password']
        read_only_fields = ['id']

    def validate_email(self, value):
        User = get_user_model()
        normalized_email = value.lower().strip()

        if User.objects.filter(email__iexact=normalized_email).exists():
            raise serializers.ValidationError('A user with this email already exists.')

        return normalized_email

    def validate_password(self, value):
        validate_password(value)

        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'\d', value):
            raise serializers.ValidationError('Password must contain at least one number.')
        if not re.search(r'[^A-Za-z0-9]', value):
            raise serializers.ValidationError('Password must contain at least one special character.')

        return value

    def create(self, validated_data):
        from .services.register_service import RegisterService

        return RegisterService().register_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )
