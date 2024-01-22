#!/usr/bin/env python3

"""Contains view for handling user signup"""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from blog.serializers.signup import SignupSerializer
from blog.models.user import MainUser as User


class SignupViewSet(viewsets.ModelViewSet):
    serializer_class = SignupSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # Check if the email or username already exists
        email_exists = User.custom_get(**{'email': serializer.validated_data['email']})
        username_exists = User.custom_get(**{'username': serializer.validated_data['username']})

        if email_exists:
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if username_exists:
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            # Use the custom save method
            user = User.custom_save(**serializer.validated_data)
            return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
