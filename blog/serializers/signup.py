#!/usr/bin/env python3

"""Contains serializer for user signup"""

from rest_framework import serializers
from blog.models.user import MainUser as User


class SignupSerializer(serializers.ModelSerializer):
    """Serializer for handling user signup"""
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'username')
        read_only_fields = ('id', 'created_at', 'updated_at')
