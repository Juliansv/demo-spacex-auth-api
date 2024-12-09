from rest_framework import serializers
from django.contrib.auth.models import User
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_first_name(self, value):
        if len(value) < 2 or len(value) > 30:
            raise serializers.ValidationError("First name must be between 2 and 30 characters.")
        return value

    def validate_last_name(self, value):
        if len(value) < 3 or len(value) > 30:
            raise serializers.ValidationError("Last name must be between 3 and 30 characters.")
        return value

    def validate_username(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("Username must be a valid email address.")
        return value

    def validate_password(self, value):
        if len(value) < 8 or len(value) > 30:
            raise serializers.ValidationError("Password must be between 8 and 30 characters.")
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).*$', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter, one uppercase letter, and one digit.")
        return value