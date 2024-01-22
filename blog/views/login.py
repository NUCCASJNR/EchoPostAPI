#!/usr/bin/env python3

"""Contains View for handling user login"""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from blog.serializers.login import LoginSerializer
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken


class LoginViewSet(viewsets.ViewSet):
    """
    Login viewset
    """
    serializer_class = LoginSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = request.data['username']
            password = request.data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                if user.verified:
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    response_data = {
                        "message": "User logged in successfully",
                        "token": str(refresh.access_token),
                        "status_code": 200
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                return Response({'error': 'User is not verified'}, status=status.HTTP_403_FORBIDDEN)
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)