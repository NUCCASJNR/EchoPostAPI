#!/usr/bin/env python3

"""Contains serializer for verifying user verification code"""

from rest_framework import serializers
from blog.models.user import MainUser as User


class EmailVerificationSerializer(serializers.ModelSerializer):
    """serializer for verifying user verification code"""
    
    verification_code = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('verification_code', )
        read_only_fields = ('id', 'created_at', 'updated_at')