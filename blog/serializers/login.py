#!/usr/bin/env python3

from rest_framework import serializers
from blog.models.user import MainUser as User



class LoginSerializer(serializers.ModelSerializer):
    """Serializer for user login"""
    
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('password', 'username')
        read_only_fields = ('id', 'created_at', 'updated_at')
