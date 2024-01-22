#!/usr/bin/env python3

"""Contains view for handling user signup"""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from blog.serializers.signup import SignupSerializer
from blog.models.user import MainUser as User
from blog.utils.email_utils import EmailUtils


class SignupViewSet(viewsets.ModelViewSet):
    serializer_class = SignupSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # Check if the email or username already exists
        email_exists = User.custom_get(**{'email': request.data['email']})
        username_exists = User.custom_get(**{'username': request.data['username']})
        code = EmailUtils.generate_verification_code()
        if email_exists:
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if username_exists:
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            user = User.custom_save(verification_code=code, **serializer.validated_data)
            EmailUtils.send_verification_email(user, code)
            response_data = {
                'message': 'Signup successful!, check your email for the verification code'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
